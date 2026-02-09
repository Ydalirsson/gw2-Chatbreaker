<template>
  <div>
    <Greeting />
    <TextEditor v-model="chatContent" ref="textEditorRef" @stack-changed="handleStackChange"
      @keyup="scheduleUpdate" />
    <p v-if="errorMessage" class="alert alert-danger" role="alert">
      {{ errorMessage }}
    </p>
    <ToolBar v-model:selected="selected" v-model:maxWordLength="charLimitInput" :totalCharacter="chatContent.length"
      :on-undo="handleUndo" :on-redo="handleRedo" :on-clear="handleClear" :undo-disabled="currentUndoLength === 0"
      :redo-disabled="currentRedoLength === 0" :insertTextAtCursor="insertTextAtCursor" />
    <SearchBar :insertTextAtCursor="insertTextAtCursor" />
    <p></p>
    <br />
    <ResultsTable :singleMessages="singleMessages" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Greeting from "./components/Greeting.vue";
import TextEditor from "./components/TextEditor.vue";
import ToolBar from "./components/ToolBar.vue";
import SearchBar from "./components/SearchBar.vue"
import ResultsTable from "./components/ResultsTable.vue";

export default defineComponent({
  name: 'App',
  components: {
    Greeting,
    TextEditor,
    ToolBar,
    SearchBar,
    ResultsTable
  },
  data() {
    return {
      chatContent: "" as string,
      singleMessages: [] as Array<{ text: string; copied: false }>,
      contentWordArray: [""] as Array<string>,
      errorMessage: "" as string,
      selected: 1 as number,
      charLimitInput: 197 as number, // actually limit is 199, but need 197 for the seperator
      currentUndoLength: 0 as number,
      currentRedoLength: 0 as number,
      updateTimer: null as number | null
    };
  },
  watch: {
    selected(newVal) {
      this.scheduleUpdate();
    },
    charLimitInput(newVal) {
      this.scheduleUpdate();
    }
  },
  methods: {
    scheduleUpdate(): void {
      if (this.updateTimer) {
        window.clearTimeout(this.updateTimer);
      }
      this.updateTimer = window.setTimeout(() => {
        this.update();
      }, 120);
    },
    update(): void {
      const MSG_CHAR_LIMIT = this.charLimitInput;
      let i = 0; // place of message
      let j = 0; // position of word
      // reset
      this.singleMessages = [{ text: "", copied: false }];
      this.contentWordArray = [""];
      this.errorMessage = "";

      // set select separation char
      let separatorChar =
        this.selected == 1 ? ">" :
          this.selected == 2 ? "+" :
            this.selected == 3 ? "-" :
              this.selected == 4 ? "~" : ">";


      // generate table if textarea is filled
      if (this.chatContent.length != 0) {
        this.contentWordArray = this.chatContent.split(" ");

        // check if every word is separable
        for (let k = 0; k < this.contentWordArray.length; k++) {
          if (this.contentWordArray[k].length > MSG_CHAR_LIMIT) {
            this.errorMessage =
              "At least one word is longer then " + MSG_CHAR_LIMIT.toString() + " characters. Try to split it with space.";
            return;
          }
        }

        while (j < this.contentWordArray.length) {
          // check if word is an emote
          if (this.contentWordArray[j] === "/emote" || this.contentWordArray[j] === "/e" || this.contentWordArray[j] === "/em" || this.contentWordArray[j] === "/me") {
            // If it's an emote, start a new message and append "/e" to it
            if (this.singleMessages[i].text.length > 0) {
              this.singleMessages[i].text += separatorChar; // finish current message
              this.singleMessages.push({ text: "", copied: false }); // start a new message
              i++;
            }
            this.singleMessages[i].text += "/e ";
            j++;

            // Process subsequent words until "##" is found
            while (j < this.contentWordArray.length && this.contentWordArray[j] !== "##") {
              // Check if adding the word exceeds the character limit
              if (this.singleMessages[i].text.length + this.contentWordArray[j].length <= MSG_CHAR_LIMIT) {
                this.singleMessages[i].text += this.contentWordArray[j].toString() + " ";
              } else {
                // If exceeds the limit, start a new message
                this.singleMessages[i].text += separatorChar; // finish Message
                this.singleMessages.push({ text: "", copied: false }); // init next message
                i++;
                j--;
                this.singleMessages[i].text += "/e "; // Start a new message with "/e"
              }
              j++;
            }

            if (this.contentWordArray[j] === "##") {
              // If it's the stop signal, start a new message
              this.singleMessages[i].text += separatorChar; // finish current message
              this.singleMessages.push({ text: "", copied: false }); // start a new message
              i++;
            }

          }
          else      // check if word is an emote
            if (this.contentWordArray[j].startsWith("/")) {
              if (this.singleMessages[i].text.length > 0) {
                this.singleMessages[i].text += separatorChar; // finish current message
                this.singleMessages.push({ text: "", copied: false }); // start a new message
                i++;
              }
              this.singleMessages[i].text += this.contentWordArray[j] + " "; // add slash command to current message
              this.singleMessages.push({ text: "", copied: false }); // start a new message
              i++;
            }
            else if (
              this.singleMessages[i].text.length +
              this.contentWordArray[j].length <=
              MSG_CHAR_LIMIT
            ) {
              this.singleMessages[i].text +=
                this.contentWordArray[j].toString() + " ";
              //console.log('Msg: ' + this.singleMessage[0])
            } else {
              this.singleMessages[i].text += separatorChar; // finish Message
              this.singleMessages.push({ text: "", copied: false }); // init next message
              i++;
              j--; // hold current word to set in next message
            }
          j++;
        }
      }
      //console.log(this.singleMessage)
    },
    insertTextAtCursor(text: string): void {
      const editorComponent = this.$refs.textEditorRef as any;
      const textarea = editorComponent?.$refs?.editor as HTMLTextAreaElement;
      const startPos = textarea.selectionStart;
      const endPos = textarea.selectionEnd;
      const textBefore = this.chatContent.substring(0, startPos);
      const textAfter = this.chatContent.substring(endPos, this.chatContent.length);
      if (startPos == 0) text = text.substring(1, text.length);
      this.chatContent = textBefore + text + textAfter;
      // set the cursor to the position after inserting the text
      const newCursorPos = startPos + text.length;
      textarea.selectionStart = newCursorPos;
      textarea.selectionEnd = newCursorPos;
      textarea.focus();
      this.update();
    },
    handleUndo() {
      const editorComponent = this.$refs.textEditorRef as any;
      editorComponent.undo();
      this.update();
    },
    handleRedo() {
      const editorComponent = this.$refs.textEditorRef as any;
      editorComponent.redo();
      this.update();
    },
    handleClear() {
      const editorComponent = this.$refs.textEditorRef as any;
      editorComponent.clearText();
      this.update();
    },
    handleStackChange({ undoLength, redoLength }: { undoLength: number; redoLength: number }) {
      this.currentUndoLength = undoLength;
      this.currentRedoLength = redoLength;
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="css">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #fff;
  background-color: #222;
  margin: 8px 8px 8px 8px;
}
</style>
