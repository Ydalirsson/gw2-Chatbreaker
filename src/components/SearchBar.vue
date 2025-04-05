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
import { defineComponent } from "vue";

export interface Item {
    [key: string]: {
        name: string;
        id: number;
        chat_link: string;
    };
}

const _itemsEN = require("../chatcodes/eng/items.json");
const _poisEN = require("../chatcodes/eng/pois.json");
const _skillsEN = require("../chatcodes/eng/skills.json");

const _itemsDE = require("../chatcodes/deu/items.json");
const _poisDE = require("../chatcodes/deu/pois.json");
const _skillsDE = require("../chatcodes/deu/skills.json");

export default defineComponent({
    name: "Toolbar",
    props: {
        insertTextAtCursor: {
            type: Function,
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
        };
    },
    watch: {
        searchInput(newInput): void {
            this.searchForLink(newInput);
        },
        updateLanguage(): void {
            this.searchResult = [];
        }
    },
    methods: {
        handleInsert(text: string): void {
            this.insertTextAtCursor(text);
        },
        searchForLink(searchInput: string): void {
            this.searchResult = [];
            if (searchInput.length < 3) return;

            // searching for english results
            if (this.cbxLangEng == "true") {
                const items = _itemsEN as Item[];
                const pois = _poisEN as Item[];
                const skills = _skillsEN as Item[];

                let i = 0;
                for (i = 0; i < items.length; i++) {
                    if (items[i].name != null) {
                        if (items[i].name.toString().includes(searchInput)) {
                            this.searchResult.push(items[i]);
                        }
                    }
                }

                for (i = 0; i < pois.length; i++) {
                    if (pois[i].name != null) {
                        if (pois[i].name.toString().includes(searchInput)) {
                            this.searchResult.push(pois[i]);
                        }
                    }
                }

                for (i = 0; i < skills.length; i++) {
                    if (skills[i].name != null) {
                        if (skills[i].name.toString().includes(searchInput)) {
                            this.searchResult.push(skills[i]);
                        }
                    }
                }
            }

            // searching for german results
            if (this.cbxLangGer == "true") {
                const items = _itemsDE as Item[];
                const pois = _poisDE as Item[];
                const skills = _skillsDE as Item[];

                let i = 0;
                for (i = 0; i < items.length; i++) {
                    if (items[i].name != null) {
                        if (items[i].name.toString().includes(searchInput)) {
                            this.searchResult.push(items[i]);
                        }
                    }
                }

                for (i = 0; i < pois.length; i++) {
                    if (pois[i].name != null) {
                        if (pois[i].name.toString().includes(searchInput)) {
                            this.searchResult.push(pois[i]);
                        }
                    }
                }

                for (i = 0; i < skills.length; i++) {
                    if (skills[i].name != null) {
                        if (skills[i].name.toString().includes(searchInput)) {
                            this.searchResult.push(skills[i]);
                        }
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

<style scoped>
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