<template>
  <div class="app-shell">
    <header class="hero">
      <div class="hero__title">
        <h1>Chatbreaker</h1>
        <Greeting class="hero__greeting" />
      </div>
      <div class="hero__meta">
        <span>Zeichen: {{ chatContent.length }}</span>
      </div>
    </header>

    <main class="layout">
      <section class="column column--left">
        <div class="panel">
          <div class="panel__header">
            <h2>Typing your text</h2>
          </div>
          <TextEditor v-model="chatContent" ref="textEditorRef" @stack-changed="handleStackChange"
            @keyup="scheduleUpdate" />
          <p v-if="errorMessage" class="alert" role="alert">
            {{ errorMessage }}
          </p>
        </div>

        <div class="panel panel--toolbar">
          <ToolBar v-model:selected="selected" v-model:maxWordLength="charLimitInput"
            :totalCharacter="chatContent.length" :on-undo="handleUndo" :on-redo="handleRedo"
            :on-clear="handleClear" :undo-disabled="currentUndoLength === 0"
            :redo-disabled="currentRedoLength === 0" />
        </div>

        <div class="panel">
          <div class="panel__header">
            <h2>Your split text</h2>
          </div>
          <ResultsTable :singleMessages="singleMessages" />
        </div>
      </section>

      <section class="column column--right">
        <div class="panel">
          <div class="panel__header">
            <h2>Adding emotes</h2>
          </div>
          <EmoteControls :insertTextAtCursor="insertTextAtCursor" />
        </div>

        <div class="panel">
          <div class="panel__header panel__header--inline">
            <h2>Adding chatlinks</h2>
            <div class="tag-group">
              <span class="tag">ger</span>
              <span class="tag">eng</span>
            </div>
          </div>
          <SearchBar :insertTextAtCursor="insertTextAtCursor" />
        </div>
      </section>
    </main>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Greeting from "./components/Greeting.vue";
import TextEditor from "./components/TextEditor.vue";
import ToolBar from "./components/ToolBar.vue";
import SearchBar from "./components/SearchBar.vue"
import ResultsTable from "./components/ResultsTable.vue";
import EmoteControls from "./components/EmoteControls.vue";

export default defineComponent({
  name: 'App',
  components: {
    Greeting,
    TextEditor,
    ToolBar,
    SearchBar,
    ResultsTable,
    EmoteControls
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
:root {
  --bg: #08090b;
  --surface: #0f1216;
  --surface-soft: #13181d;
  --border: #1f262d;
  --text: #f5f5f5;
  --muted: #9aa3aa;
  --accent: #0f2dd9;
  --accent-strong: #0a1fb0;
  --danger: #e04b4b;
  --shadow: 0 16px 40px rgba(0, 0, 0, 0.35);
}

*,
*::before,
*::after {
  box-sizing: border-box;
}

#app {
  font-family: "Cinzel Decorative", "Goudy Old Style", serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--text);
  background: radial-gradient(circle at top left, #11161d 0%, #07080a 52%, #050607 100%);
  min-height: 100vh;
}

body {
  margin: 0;
  background: var(--bg);
}

.app-shell {
  padding: 28px 32px 48px;
}

.hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.hero__title h1 {
  margin: 0;
  font-size: clamp(2.2rem, 3vw, 3.6rem);
  letter-spacing: 0.08em;
}

.hero__title p {
  margin: 4px 0 0;
  font-size: 1rem;
  color: var(--muted);
  font-family: "Georgia", serif;
}

.hero__meta {
  font-size: 1rem;
  color: var(--muted);
  font-family: "Georgia", serif;
}

.hero__greeting {
  margin-top: 8px;
  color: var(--muted);
  font-size: 0.85rem;
  font-family: "Georgia", serif;
}

.layout {
  display: grid;
  grid-template-columns: 1.25fr 0.75fr;
  gap: 28px;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 18px;
  box-shadow: var(--shadow);
}

.panel--toolbar {
  padding: 12px 16px;
}

.panel__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.panel__header--inline {
  align-items: center;
  gap: 16px;
}

.panel__header h2 {
  font-size: 1.1rem;
  margin: 0;
  color: var(--text);
  font-family: "Georgia", serif;
}

.tag-group {
  display: inline-flex;
  gap: 8px;
}

.tag {
  background: #94a0a8;
  color: #0d1013;
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 0.75rem;
  letter-spacing: 0.04em;
  font-family: "Georgia", serif;
}

.alert {
  margin-top: 12px;
  padding: 10px 12px;
  border-radius: 10px;
  background: rgba(224, 75, 75, 0.14);
  color: #ffb3b3;
  border: 1px solid rgba(224, 75, 75, 0.4);
  font-family: "Georgia", serif;
}

@media (max-width: 1100px) {
  .layout {
    grid-template-columns: 1fr;
  }
}
</style>
