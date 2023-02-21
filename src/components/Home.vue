<template>
  <div class="home">
    <div>
      <p style="font-size: 10pt">
        Hello, today is {{ currentMouvDate() }}, {{ currentElonDate() }},
        {{ currentCantDate() }}
      </p>
    </div>

    <div>
      <textarea
        id="chatContent"
        v-model="chatContent"
        ref="chatEdit"
        placeholder="Insert something in me OwO"
        cols="50"
        rows="10"
        class="form-control"
        @keyup="update"
      ></textarea>

      <p v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </p>

      <ul class="controlBar">
        <li>
          <button
            type="button"
            class="btn btn-outline-danger"
            style="margin-top: 4px"
            @click="deleteAreaInput"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              fill="currentColor"
              class="bi bi-trash"
              viewBox="0 0 16 16"
            >
              <path
                d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
              />
              <path
                fill-rule="evenodd"
                d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
              />
            </svg>
            Delete
          </button>
        </li>
        <li>
          <select
            class="form-select form-select-sm"
            style="margin-top: 4px; width: 110px; height: 38px"
            v-model="selected"
            @change="update"
          >
            <option disabled value="0">Separator</option>
            <option value="1">> (default)</option>
            <option value="2">+</option>
            <option value="3">-</option>
            <option value="4">~</option>
          </select>
        </li>
        <li>
          <ul
            id="emoteListID"
            class="list-group"
            @click="changeEmoteList"
            v-if="listCollapsed"
          >
            <li class="list-group-item py-0">/beckon</li>
            <li class="list-group-item py-0">/bow</li>
            <li class="list-group-item py-0">/cheer</li>
            <li class="list-group-item py-0">/cower</li>
            <li class="list-group-item py-0">/crossarms</li>
            <li class="list-group-item py-0">/cry</li>
            <li class="list-group-item py-0">/dance</li>
            <li class="list-group-item py-0">/facepalm</li>
            <li class="list-group-item py-0">/upset</li>
            <li class="list-group-item py-0">/geargrind</li>
            <li class="list-group-item py-0">/kneel</li>
            <li class="list-group-item py-0">/laugh</li>
            <li class="list-group-item py-0">/no</li>
            <li class="list-group-item py-0">/playdead</li>
            <li class="list-group-item py-0">/point</li>
            <li class="list-group-item py-0">/ponder</li>
            <li class="list-group-item py-0">/rockout</li>
            <li class="list-group-item py-0">/sad</li>
            <li class="list-group-item py-0">/salute</li>
            <li class="list-group-item py-0">/shiver</li>
            <li class="list-group-item py-0">/shiverplus</li>
            <li class="list-group-item py-0">/shrug</li>
            <li class="list-group-item py-0">/shuffle</li>
            <li class="list-group-item py-0">/sit</li>
            <li class="list-group-item py-0">/sleep</li>
            <li class="list-group-item py-0">/step</li>
            <li class="list-group-item py-0">/stretch</li>
            <li class="list-group-item py-0">/surprised</li>
            <li class="list-group-item py-0">/talk</li>
            <li class="list-group-item py-0">/thanks</li>
            <li class="list-group-item py-0">/thank</li>
            <li class="list-group-item py-0">/thx</li>
            <li class="list-group-item py-0">/ty</li>
            <li class="list-group-item py-0">/threaten</li>
            <li class="list-group-item py-0">/wave</li>
            <li class="list-group-item py-0">/yes</li>
            <li class="list-group-item py-0">/e</li>
            <li class="list-group-item py-0">/em</li>
            <li class="list-group-item py-0">/emote</li>
            <li class="list-group-item py-0">/me</li>
            <span class="tooltiptext">Click to collapse</span>
          </ul>
          <ul id="emoteID" class="list-group" @click="changeEmoteList" v-else>
            <li class="list-group-item">List of emotes</li>
            <span class="tooltiptext">Click to expand</span>
          </ul>
        </li>

        <li>
          <div>total characters: {{ totalCharacter }}</div>
        </li>
      </ul>
    </div>

    <div class="ac-container">
        <input
          class="form-group"
          type="search"
          placeholder="Search for chatlink"
          v-model="searchInput"
          @blur="blur"
          @input="inputChanged"
          @focus="focus"
          @keyup.esc="escape"
          @keyup.enter="enter"
          @keydown.tab="enter"
          @keydown.up="up"
          @keydown.down="down"
        />

        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            id="cbxLangEng"
            v-model="cbxLangEng"
            true-value="true"
            false-value="false"
            checked
            @change="upateLanguage"
          />
          <label class="form-check-label" for="cbxLangEng">eng</label>
        </div>
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            id="cbxLangGer"
            v-model="cbxLangGer"
            true-value="true"
            false-value="false"
            @change="upateLanguage"
          />
          <label class="form-check-label" for="cbxLangGer">ger</label>
        </div>

      <div class="ac-filtered-items" v-if="showItems">
        <div
          class="ac-filtered-item"
          :class="{ 'ac-filtered-item__hovered': index === cursor }"
          v-for="(item, index) in searchResult"
          :key="index"
          @click="selectItem(item)"
          @mouseover="cursor = index"
        >
          <div>
            {{ item.name }},
            <span style="font-size: 8pt">{{ item.chat_link }}</span>
          </div>
        </div>
      </div>
    </div>

    <p></p>
    <br />

    <div class="table-responsive">
      <table class="table table-dark table-striped">
        <tbody>
          <tr v-for="msg in singleMessage" v-bind:key="msg.text">
            <td>{{ msg.text }}</td>
            <td>
              <button
                type="button"
                @click="onCopy(msg)"
                v-if="msg.text"
                class="btn btn-outline-info"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  fill="currentColor"
                  class="bi bi-clipboard"
                  viewBox="0 0 16 16"
                >
                  <path
                    d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"
                  ></path>
                  <path
                    d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"
                  ></path>
                </svg>
                Copy
              </button>
            </td>
            <td v-if="msg.copied">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="32"
                height="32"
                fill="green"
                class="bi bi-check"
                viewBox="0 0 16 16"
              >
                <path
                  d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z"
                />
              </svg>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { writeText } from "@tauri-apps/api/clipboard";

export interface Item {
  [key: string]: {
    name: string;
    id: number;
    chat_link: string;
  };
}

const _colorsEN = require("../chatcodes/eng/colors.json");
const _itemsEN = require("../chatcodes/eng/items.json");
const _poisEN = require("../chatcodes/eng/pois.json");
const _recipesEN = require("../chatcodes/eng/recipes.json");
const _skillsEN = require("../chatcodes/eng/skills.json");
const _skinsEN = require("../chatcodes/eng/skins.json");
const _traitsEN = require("../chatcodes/eng/traits.json");

const _colorsDE = require("../chatcodes/deu/colors.json");
const _itemsDE = require("../chatcodes/deu/items.json");
const _poisDE = require("../chatcodes/deu/pois.json");
const _recipesDE = require("../chatcodes/deu/recipes.json");
const _skillsDE = require("../chatcodes/deu/skills.json");
const _skinsDE = require("../chatcodes/deu/skins.json");
const _traitsDE = require("../chatcodes/deu/traits.json");

export default defineComponent({
  name: "home",
  data() {
    return {
      chatContent: "" as string,
      contentWordArray: [""] as Array<string>,
      singleMessage: [] as Array<{ text: ""; copied: false }>,
      errorMessage: "" as string,
      totalCharacter: 0 as number,
      selected: "0" as string,
      listCollapsed: false as boolean,
      searchResult: [] as Array<Item>,
      searchInput: "" as string,
      showItems: false as boolean,
      cursor: -1 as number,
      cbxLangEng: "true" as string,
      cbxLangGer: "false" as string,
    };
  },
  watch: {
    searchInput(newInput) {
      this.searchForLink(newInput);
    },
    upateLanguage() {
      this.searchResult = [];
    },
  },
  methods: {
    changeEmoteList(): void {
      this.listCollapsed = !this.listCollapsed;
    },
    currentMouvDate() {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(
        dateNow.getFullYear(),
        0,
        1,
        23,
        59,
        59,
        999
      );
      let dayOfYear =
        Math.floor(dateNow.getTime() - currentYear.getTime()) /
        1000 /
        60 /
        60 /
        24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = "";
      let mouveCalenderDay = 0;
      if (1 <= dayOfYear && dayOfYear <= 90) {
        season = "Zephyr";
        mouveCalenderDay = dayOfYear;
      } else if (91 <= dayOfYear && dayOfYear <= 180) {
        season = "Phoenix";
        mouveCalenderDay = dayOfYear - 90;
      } else if (181 <= dayOfYear && dayOfYear <= 270) {
        season = "Scion";
        mouveCalenderDay = dayOfYear - 180;
      } else if (271 <= dayOfYear && dayOfYear <= 366) {
        season = "Colossus";
        mouveCalenderDay = dayOfYear - 270;
      }
      return (
        mouveCalenderDay +
        " " +
        season +
        " " +
        (dateNow.getFullYear() - 687) +
        " A.E."
      );
    },
    currentElonDate() {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(
        dateNow.getFullYear(),
        0,
        1,
        23,
        59,
        59,
        999
      );
      let dayOfYear =
        Math.floor(dateNow.getTime() - currentYear.getTime()) /
        1000 /
        60 /
        60 /
        24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = "";
      let mouveCalenderDay = 0;
      if (1 <= dayOfYear && dayOfYear <= 90) {
        season = "Zephyr";
        mouveCalenderDay = dayOfYear;
      } else if (91 <= dayOfYear && dayOfYear <= 180) {
        season = "Phoenix";
        mouveCalenderDay = dayOfYear - 90;
      } else if (181 <= dayOfYear && dayOfYear <= 270) {
        season = "Scion";
        mouveCalenderDay = dayOfYear - 180;
      } else if (271 <= dayOfYear && dayOfYear <= 366) {
        season = "Colossus";
        mouveCalenderDay = dayOfYear - 270;
      }
      return (
        mouveCalenderDay +
        " " +
        season +
        " " +
        (dateNow.getFullYear() - 687 + 200) +
        " D.Z."
      );
    },
    currentCantDate() {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(
        dateNow.getFullYear(),
        0,
        1,
        23,
        59,
        59,
        999
      );
      let dayOfYear =
        Math.floor(dateNow.getTime() - currentYear.getTime()) /
        1000 /
        60 /
        60 /
        24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = "";
      let mouveCalenderDay = dateNow.getDate();

      switch (dateNow.getMonth()) {
        case 0:
          season = "Changhai";
          break;
        case 1:
          season = "Zhoyo";
          break;
        case 2:
          season = "Nongkam";
          break;
        case 3:
          season = "Zalfawn";
          break;
        case 4:
          season = "Saita";
          break;
        case 5:
          season = "Mikan";
          break;
        case 6:
          season = "Nemnai";
          break;
        case 7:
          season = "Beibacah";
          break;
        case 8:
          season = "Suzhen";
          break;
        case 9:
          season = "Yundinfang";
          break;
        case 10:
          season = "Songtahn";
          break;
        case 11:
          season = "Kainengtah";
          break;

        default:
          season = "";
          break;
      }

      return (
        mouveCalenderDay +
        " " +
        season +
        " " +
        (dateNow.getFullYear() - 687 + 510) +
        " C.K."
      );
    },
    deleteAreaInput(): void {
      this.chatContent = "";
      this.singleMessage = [{ text: "", copied: false }];
      this.contentWordArray = [""];
      this.errorMessage = "";

      this.totalCharacter = this.chatContent.length;
      (this.$refs.chatEdit as HTMLElement).focus();
    },
    update(): void {
      const MSG_CHAR_LIMIT = 197; // character limit per single chat message (in gw2 it's 199, but 197 needed to add ' >' automatically
      let i = 0; // place of message
      let j = 0; // position of word
      let separatorChar = ">";
      // reset
      this.singleMessage = [{ text: "", copied: false }];
      this.contentWordArray = [""];
      this.errorMessage = "";

      // set select separation char
      if (this.selected == "1") separatorChar = ">";
      else if (this.selected == "2") separatorChar = "+";
      else if (this.selected == "3") separatorChar = "-";
      else if (this.selected == "4") separatorChar = "~";
      else separatorChar = ">";

      this.totalCharacter = this.chatContent.length;
      // generate table if textarea is filled
      if (this.chatContent.length != 0) {
        this.contentWordArray = this.chatContent.split(" ");

        // check if every word is separable
        for (let k = 0; k < this.contentWordArray.length; k++) {
          if (this.contentWordArray[k].length > MSG_CHAR_LIMIT) {
            this.errorMessage =
              "At least one word is longer then 197 characters. Try to split it with space.";
            return;
          }
        }

        while (j < this.contentWordArray.length) {
          // check if word fits in message
          if (
            this.singleMessage[i].text.length +
              this.contentWordArray[j].length <=
            MSG_CHAR_LIMIT
          ) {
            this.singleMessage[i].text +=
              this.contentWordArray[j].toString() + " ";
            //console.log('Msg: ' + this.singleMessage[0])
          } else {
            this.singleMessage[i].text += separatorChar; // finish Message
            this.singleMessage.push({ text: "", copied: false }); // init next message
            i++;
            j--; // hold current word to set in next message
          }
          j++;
        }
      }
      //console.log(this.singleMessage)
    },
    onCopy(msg: { text: ""; copied: boolean }): void {
      //console.log("CopyText" + msg);
      writeText(msg.text);
      msg.copied = true;
    },
    searchForLink(searchInput: string): void {
      this.searchResult = [];
      if (searchInput.length < 3) return;

      // searching for english results
      if (this.cbxLangEng == "true") {
        const colors = _colorsEN as Item[];
        const items = _itemsEN as Item[];
        const pois = _poisEN as Item[];
        const recipes = _recipesEN as Item[];
        const skills = _skillsEN as Item[];
        const skins = _skinsEN as Item[];
        const traits = _traitsEN as Item[];

        let i = 0;
        for (i = 0; i < colors.length; i++) {
          if (colors[i].name != null) {
            if (colors[i].name.toString().includes(searchInput)) {
              this.searchResult.push(colors[i]);
            }
          }

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

          for (i = 0; i < recipes.length; i++) {
            if (recipes[i].name != null) {
              if (recipes[i].name.toString().includes(searchInput)) {
                this.searchResult.push(recipes[i]);
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
          for (i = 0; i < skins.length; i++) {
            if (skins[i].name != null) {
              if (skins[i].name.toString().includes(searchInput)) {
                this.searchResult.push(skins[i]);
              }
            }
          }
          for (i = 0; i < traits.length; i++) {
            if (traits[i].name != null) {
              if (traits[i].name.toString().includes(searchInput)) {
                this.searchResult.push(traits[i]);
              }
            }
          }
        }
      }

      // searching for german results
      if (this.cbxLangGer == "true") {
        const colors = _colorsDE as Item[];
        const items = _itemsDE as Item[];
        const pois = _poisDE as Item[];
        const recipes = _recipesDE as Item[];
        const skills = _skillsDE as Item[];
        const skins = _skinsDE as Item[];
        const traits = _traitsDE as Item[];

        let i = 0;
        for (i = 0; i < colors.length; i++) {
          if (colors[i].name != null) {
            if (colors[i].name.toString().includes(searchInput)) {
              this.searchResult.push(colors[i]);
            }
          }

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

          for (i = 0; i < recipes.length; i++) {
            if (recipes[i].name != null) {
              if (recipes[i].name.toString().includes(searchInput)) {
                this.searchResult.push(recipes[i]);
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
          for (i = 0; i < skins.length; i++) {
            if (skins[i].name != null) {
              if (skins[i].name.toString().includes(searchInput)) {
                this.searchResult.push(skins[i]);
              }
            }
          }
          for (i = 0; i < traits.length; i++) {
            if (traits[i].name != null) {
              if (traits[i].name.toString().includes(searchInput)) {
                this.searchResult.push(traits[i]);
              }
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
        this.chatContent += " " + item.chat_link.toString();
        this.update();
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
      if (this.cursor > -1) {
        this.cursor--;
        this.$el.getElementsByClassName("ac-filtered-item")[this.cursor];
      }
    },
    down(): void {
      this.showItems = true;
      if (this.cursor < this.searchResult.length) {
        this.cursor++;
        this.$el.getElementsByClassName("ac-filtered-item")[this.cursor];
      }
    },
    escape(): void {
      this.showItems = !this.showItems;
    },
  },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
textarea:focus {
  background-color: #23272a;
  color: #fff;
}
input[type="text"],
textarea {
  background-color: #23272a;
  color: #fff;
}
select {
  background-color: #375a7f;
  color: #fff;
}
.controlBar {
  display: flex;
  justify-content: space-between;
  list-style: none;
  padding-left: 0;
}
#emoteID .tooltiptext,
#emoteListID .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}
#emoteID:hover .tooltiptext,
#emoteListID:hover .tooltiptext {
  visibility: visible;
}
#emoteID,
#emoteListID {
  font-size: 10pt;
}

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
