<template>
  <div class="home">
    <div>
      <p style="font-size: 10pt">
        Hello, today is {{ currentMouvDate() }}, {{ currentElonDate() }},
        {{ currentCantDate() }}
      </p>
    </div>

    <div>
      <textarea id="chatContent" v-model="chatContent" ref="chatEdit" placeholder="Insert text here" cols="50"
        rows="10" class="form-control" @keyup="update"></textarea>

    <button class="btn btn-secondary btn-sm" @click="undo" :disabled="undoStack.length === 0" title="Undo (Ctrl+Z / Cmd+Z)">Undo</button>
    <button class="btn btn-secondary btn-sm" @click="redo" :disabled="redoStack.length === 0" title="Redo (Ctrl+Y / Cmd+Shift+Z)">Redo</button>

      <p v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </p>

      <ul class="controlBar">
        <li>
          <button type="button" class="btn btn-outline-danger" style="margin-top: 4px" @click="deleteAreaInput">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash"
              viewBox="0 0 16 16">
              <path
                d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
              <path fill-rule="evenodd"
                d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
            </svg>
            Delete
          </button>
        </li>
        <li>
          <select class="form-select form-select-sm" style="margin-top: 4px; width: 110px; height: 38px"
            v-model="selected" @change="update">
            <option disabled value="0">Separator</option>
            <option value="1">> (default)</option>
            <option value="2">+</option>
            <option value="3">-</option>
            <option value="4">~</option>
          </select>
        </li>

        <li>
          <input type="number" placeholder="Limit" value="197" min="3" class="form-control form-control-sm"
            style="margin-top: 4px; width: 110px; height: 38px" data-toggle="tooltip" data-placement="bottom" title="This field determines the number of characters that can appear in a message. Can be set as required.
            - GW2-Mode: 197
            - Discord-Mode: 1998" v-model="charLimitInput" @change="update">
        </li>

        <li>
          <button type="button" class="btn btn-primary" style="margin-top: 4px"
            @click="insertTextAtCursor(' /e ')">Start emote</button>
          <button type="button" class="btn btn-primary" style="margin-top: 4px" @click="insertTextAtCursor(' ## ')">End
            emote</button>
        </li>

        <li>
          <ul id="emoteListID" class="list-group" @click="changeEmoteList" v-if="listCollapsed">
            <span class="tooltiptext">Click to collapse</span>
            <li v-for="(emote, index) in emotes" :key="index" class="list-group-item py-0"
              @click="insertTextAtCursor(' ' + emote + ' ')">{{ emote }}</li>
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
      <input class="form-group" type="search" placeholder="Search for chatlink" title="Input is case sensitive!"
        v-model="searchInput" @blur="blur" @input="inputChanged" @focus="focus" @keyup.esc="escape" @keyup.enter="enter"
        @keydown.tab="enter" @keydown.up="up" @keydown.down="down" />

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
          v-for="(item, index) in searchResult" :key="index" @click="selectItem(item)" @mouseover="cursor = index">
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
              <button type="button" @click="onCopy(msg)" v-if="msg.text" class="btn btn-outline-info">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                  class="bi bi-clipboard" viewBox="0 0 16 16">
                  <path
                    d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z">
                  </path>
                  <path
                    d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z">
                  </path>
                </svg>
                Copy
              </button>
            </td>
            <td v-if="msg.copied">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="green" class="bi bi-check"
                viewBox="0 0 16 16">
                <path
                  d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z" />
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
  name: "home",
  data() {
    return {
      undoStack: [] as string[],
      redoStack: [] as string[],
      chatContent: "" as string,
      contentWordArray: [""] as Array<string>,
      singleMessage: [] as Array<{ text: string; copied: false }>,
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
      charLimitInput: 197 as number, // actually limit is 199, but need 197 for the seperator
      emotes: [
        "/beckon",
        "/bless",
        "/bow",
        "/cheer",
        "/cower",
        "/crossarms",
        "/cry",
        "/dance",
        "/facepalm",
        "/upset",
        "/geargrind",
        "/heroic",
        "/hiss",
        "/kneel",
        "/laugh",
        "/magicjuggle",
        "/no",
        "/paper",
        "/playdead",
        "/point",
        "/ponder",
        "/possessed",
        "/rank",
        "/readbook",
        "/rock",
        "/rockout",
        "/sad",
        "/salute",
        "/scissors",
        "/scis",
        "/serve",
        "/shiver",
        "/shiverplus",
        "/shrug",
        "/shuffle",
        "/sipcoffee",
        "/sit",
        "/sleep",
        "/step",
        "/stretch",
        "/surprised",
        "/talk",
        "/thanks",
        "/thank",
        "/thx",
        "/ty",
        "/threaten",
        "/wave",
        "/yes",
        "/e",
        "/em",
        "/emote",
        "/me"
      ]

    };
  },
  watch: {
    searchInput(newInput): void {
      this.searchForLink(newInput);
    },
    updateLanguage(): void {
      this.searchResult = [];
    },
  },
  methods: {
    changeEmoteList(): void {
      this.listCollapsed = !this.listCollapsed;
    },
    currentMouvDate(): string {
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
    currentElonDate(): string {
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
    currentCantDate(): string {
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
      this.redoStack = [""];
      this.undoStack = [""];

      this.totalCharacter = this.chatContent.length;
      (this.$refs.chatEdit as HTMLElement).focus();
    },
    update(): void {
      const MSG_CHAR_LIMIT = this.charLimitInput; // character limit per single chat message (in gw2 it's 199, but 197 needed to add ' >' automatically
      let i = 0; // place of message
      let j = 0; // position of word
      let separatorChar = ">";
      // reset
      this.singleMessage = [{ text: "", copied: false }];
      this.contentWordArray = [""];
      this.errorMessage = "";
      if (this.undoStack[this.undoStack.length - 1] !== this.chatContent) {
        this.undoStack.push(this.chatContent);
      }
      this.redoStack = []; // Reset redo stack on new input

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
              "At least one word is longer then " + MSG_CHAR_LIMIT.toString() + "characters. Try to split it with space.";
            return;
          }
        }

        while (j < this.contentWordArray.length) {
          // check if word is an emote
          if (this.contentWordArray[j] === "/emote" || this.contentWordArray[j] === "/e" || this.contentWordArray[j] === "/em" || this.contentWordArray[j] === "/me") {
            // If it's an emote, start a new message and append "/e" to it
            if (this.singleMessage[i].text.length > 0) {
              this.singleMessage[i].text += separatorChar; // finish current message
              this.singleMessage.push({ text: "", copied: false }); // start a new message
              i++;
            }
            this.singleMessage[i].text += "/e ";
            j++;

            // Process subsequent words until "##" is found
            while (j < this.contentWordArray.length && this.contentWordArray[j] !== "##") {
              // Check if adding the word exceeds the character limit
              if (this.singleMessage[i].text.length + this.contentWordArray[j].length <= MSG_CHAR_LIMIT) {
                this.singleMessage[i].text += this.contentWordArray[j].toString() + " ";
              } else {
                // If exceeds the limit, start a new message
                this.singleMessage[i].text += separatorChar; // finish Message
                this.singleMessage.push({ text: "", copied: false }); // init next message
                i++;
                j--;
                this.singleMessage[i].text += "/e "; // Start a new message with "/e"
              }
              j++;
            }

            if (this.contentWordArray[j] === "##") {
              // If it's the stop signal, start a new message
              this.singleMessage[i].text += separatorChar; // finish current message
              this.singleMessage.push({ text: "", copied: false }); // start a new message
              i++;
            }

          }
          else      // check if word is an emote
            if (this.contentWordArray[j].startsWith("/")) {
              if (this.singleMessage[i].text.length > 0) {
                this.singleMessage[i].text += separatorChar; // finish current message
                this.singleMessage.push({ text: "", copied: false }); // start a new message
                i++;
              }
              this.singleMessage[i].text += this.contentWordArray[j] + " "; // add slash command to current message
              this.singleMessage.push({ text: "", copied: false }); // start a new message
              i++;
            }
            else if (
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
      navigator.clipboard.writeText(msg.text);
      msg.copied = true;
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
    },
    insertTextAtCursor(text: string): void {
      const textarea = this.$refs.chatEdit as HTMLTextAreaElement;
      const startPos = textarea.selectionStart;
      const endPos = textarea.selectionEnd;
      const textBefore = this.chatContent.substring(0, startPos);
      const textAfter = this.chatContent.substring(endPos, this.chatContent.length);
      if (startPos == 0) text = text.substring(1, text.length);
      this.chatContent = textBefore + text + textAfter;
      // Setze den Cursor an die Position nach dem Einfügen des Textes
      const newCursorPos = startPos + text.length;
      textarea.selectionStart = newCursorPos;
      textarea.selectionEnd = newCursorPos;
      textarea.focus();
      // Trigger das "update"-Event
      this.update();
    },
    undo(): void {
      if (this.undoStack.length > 0) {
        if (this.undoStack.length > 1) {
        this.redoStack.push(this.undoStack.pop() ?? "");
        this.chatContent = this.undoStack[this.undoStack.length - 1];
      } else if (this.undoStack.length === 1) {
        this.redoStack.push(this.chatContent);
        this.chatContent = "";
      }
      }
    },
    redo(): void {
      if (this.redoStack.length > 0) {
        this.undoStack.push(this.chatContent);
        this.chatContent = this.redoStack.pop() ?? "";
      }
    },
    handleKeydown(event: KeyboardEvent) {
      if (event.ctrlKey || event.metaKey) {
        if (event.key === "z") {
          event.preventDefault();
          this.undo();
        } else if (event.key === "y" || (event.shiftKey && event.key === "Z")) {
          event.preventDefault();
          this.redo();
        }
      }
    },
    mounted() {
    window.addEventListener("keydown", this.handleKeydown);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
  },

  }
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
  position: static;
  z-index: 1;
  top: 20px;
  /* Beispiel: Verschiebung um 20px nach unten */
  left: 0;
  /* Beispiel: Tooltip linksbündig */
}

#emoteID:hover .tooltiptext,
#emoteListID:hover .tooltiptext,
#emoteID.active .tooltiptext,
#emoteListID.active .tooltiptext {
  visibility: visible;
}

#emoteID,
#emoteListID {
  font-size: 10pt;
}

#emoteListID {
  position: relative;
  top: -25px;
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
