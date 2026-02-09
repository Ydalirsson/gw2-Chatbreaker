<template>
    <div class="ac-container">
        <input class="form-group" type="search" placeholder="Search for chatlink" title="Input is case sensitive!"
            v-model="searchInput" @blur="blur" @input="inputChanged" @focus="focus" @keyup.esc="escape"
            @keyup.enter="enter" @keydown.tab="enter" @keydown.up="up" @keydown.down="down" />

        <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="cbxLangEng" v-model="cbxLangEng" true-value="true"
                false-value="false" checked @change="updateLanguage" />
            <label class="form-check-label" for="cbxLangEng">eng</label>
        </div>
        <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="cbxLangGer" v-model="cbxLangGer" true-value="true"
                false-value="false" @change="updateLanguage" />
            <label class="form-check-label" for="cbxLangGer">ger</label>
        </div>

        <div class="ac-filtered-items" v-if="showItems">
            <div class="ac-filtered-item" :class="{ 'ac-filtered-item__hovered': index === cursor }"
                v-for="(item, index) in searchResult" :key="index" @click="selectItem(item)"
                @mouseover="cursor = index">
                <div>
                    {{ item.name }},
                    <span style="font-size: 8pt">{{ item.chat_link }}</span>
                </div>
            </div>
        </div>
    </div>

</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export interface Item {
    name: string;
    id: number;
    chat_link: string;
}

interface SearchItem extends Item {
    nameLower: string;
}

import itemsEN from "../chatcodes/eng/items.json";
import poisEN from "../chatcodes/eng/pois.json";
import skillsEN from "../chatcodes/eng/skills.json";

import itemsDE from "../chatcodes/deu/items.json";
import poisDE from "../chatcodes/deu/pois.json";
import skillsDE from "../chatcodes/deu/skills.json";

export default defineComponent({
    name: "SearchBar",
    props: {
        insertTextAtCursor: {
            type: Function as PropType<(text: string) => void>,
            required: true,
        }
    },
    data() {
        return {
            searchResult: [] as Array<Item>,
            searchInput: "" as string,
            showItems: false as boolean,
            cursor: -1 as number,
            cbxLangEng: "true" as string,
            cbxLangGer: "false" as string,
            maxResults: 50 as number,
            searchTimer: null as number | null,
            engItems: [] as Array<SearchItem>,
            deuItems: [] as Array<SearchItem>,
            engIndex: new Map<string, Array<SearchItem>>(),
            deuIndex: new Map<string, Array<SearchItem>>()
        };
    },
    watch: {
        searchInput(newInput): void {
            this.scheduleSearch(newInput);
        },
        cbxLangEng(): void {
            this.searchResult = [];
        },
        cbxLangGer(): void {
            this.searchResult = [];
        },
    },
    created() {
        this.engItems = this.buildSearchItems([itemsEN, poisEN, skillsEN]);
        this.deuItems = this.buildSearchItems([itemsDE, poisDE, skillsDE]);
        this.engIndex = this.buildIndex(this.engItems);
        this.deuIndex = this.buildIndex(this.deuItems);
    },
    methods: {
        buildSearchItems(sources: Array<Item[] | unknown>): Array<SearchItem> {
            const flattened: Array<SearchItem> = [];
            for (const source of sources) {
                const items = source as Item[];
                for (let i = 0; i < items.length; i++) {
                    const name = items[i].name ?? "";
                    flattened.push({
                        ...items[i],
                        nameLower: name.toString().toLowerCase()
                    });
                }
            }
            return flattened;
        },
        buildIndex(items: Array<SearchItem>): Map<string, Array<SearchItem>> {
            const index = new Map<string, Array<SearchItem>>();
            for (let i = 0; i < items.length; i++) {
                const key = items[i].nameLower.slice(0, 3);
                if (!index.has(key)) {
                    index.set(key, []);
                }
                index.get(key)?.push(items[i]);
            }
            return index;
        },
        scheduleSearch(searchInput: string): void {
            if (this.searchTimer) {
                window.clearTimeout(this.searchTimer);
            }
            this.searchTimer = window.setTimeout(() => {
                this.searchForLink(searchInput);
            }, 180);
        },
        handleInsert(text: string): void {
            this.insertTextAtCursor(text);
        },
        searchForLink(searchInput: string): void {
            this.searchResult = [];
            if (searchInput.length < 3) return;

            const queryLower = searchInput.toLowerCase();
            let remaining = this.maxResults;

            // searching for english results
            if (this.cbxLangEng == "true") {
                const key = queryLower.slice(0, 3);
                const candidates = this.engIndex.get(key) ?? this.engItems;
                for (let i = 0; i < candidates.length && remaining > 0; i++) {
                    if (candidates[i].nameLower.includes(queryLower)) {
                        this.searchResult.push(candidates[i]);
                        remaining--;
                    }
                }
            }

            // searching for german results
            if (this.cbxLangGer == "true" && remaining > 0) {
                const key = queryLower.slice(0, 3);
                const candidates = this.deuIndex.get(key) ?? this.deuItems;
                for (let i = 0; i < candidates.length && remaining > 0; i++) {
                    if (candidates[i].nameLower.includes(queryLower)) {
                        this.searchResult.push(candidates[i]);
                        remaining--;
                    }
                }
            }
        },
        selectItem(item: Item): void {
            if (item) {
                this.searchInput = item.name.toString();
                this.$emit("inputChanged", this.searchInput);
                this.showItems = false;
                this.insertTextAtCursor(" " + item.chat_link.toString());
            }
        },
        blur(): void {
            setTimeout(() => (this.showItems = false), 200);
        },
        focus(): void {
            this.showItems = true;
        },
        inputChanged(): void {
            this.showItems = true;
            this.$emit("inputChanged", this.searchInput);
        },
        enter(): void {
            if (this.showItems && this.searchResult[this.cursor]) {
                this.selectItem(this.searchResult[this.cursor]);
                this.$emit("inputChanged", this.searchInput);
                this.showItems = false;
            }
        },
        up(): void {
            if (this.cursor > 0) {
                this.cursor--;
                this.$el.getElementsByClassName("ac-filtered-item")[this.cursor];
                const element = this.$el.getElementsByClassName("ac-filtered-item")[this.cursor];
                element.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
            }
        },
        down(): void {
            this.showItems = true;
            if (this.cursor < this.searchResult.length - 1) {
                this.cursor++;
                const element = this.$el.getElementsByClassName("ac-filtered-item")[this.cursor];
                element.scrollIntoView({ behavior: "smooth", block: "center", inline: "center" });
            }
        },
        escape(): void {
            this.showItems = !this.showItems;
        }
    }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
.ac-container {
    position: relative;
    display: grid;
    grid-template-columns: auto auto auto;
    justify-content: start;
}

.ac-filtered-items {
    position: relative;
    top: 0;
    left: 0;
    right: 0;
    width: auto;
    grid-row: 2;
    padding: 2px;
    text-align: left;
    border: 2px solid #ececec;
    border-top: none;
    border-radius: 2px;
    max-height: 400px;
    overflow-y: auto;
    z-index: 9999;
    font-size: 10pt;
}

.ac-container .ac-filtered-items .ac-filtered-item {
    cursor: pointer;
}

.ac-container .ac-filtered-items .ac-filtered-item:hover,
.ac-container .ac-filtered-items .ac-filtered-item__hovered {
    background-color: #eee;
    color: #101010;
}
</style>
