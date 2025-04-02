<template>
  <div>
    <Greeting />
    <TextEditor v-model="chatContent" />
    <Toolbar/>
    <EmoteControles/>
    <ResultsTable :messages="singleMessage" />
  </div>
</template>

<script lang="ts">
import Greeting from "./Greeting.vue";
import TextEditor from "./TextEditor.vue";
import Toolbar from "./Toolbar.vue";
import EmoteControles from "./EmoteControles.vue";
import SearchBar from "./SearchBar.vue"
import ResultsTable from "./ResultsTable.vue";

export default {
  components: {
    Greeting,
    TextEditor,
    Toolbar,
    EmoteControles,
    SearchBar,
    ResultsTable
  },
  data() {
    return {
      chatContent: "" as string,
      singleMessage: [] as Array<{ text: string; copied: false }>,
      contentWordArray: [""] as Array<string>,
      errorMessage: "" as string,
      charLimitInput: 197 as number // actually limit is 199, but need 197 for the seperator
    };
  },
  methods: {
    update(): void {
      const MSG_CHAR_LIMIT = this.charLimitInput; // character limit per single chat message (in gw2 it's 199, but 197 needed to add ' >' automatically
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
    }
  }
};
</script>
