<template>
  <div class="text-editor">
    <textarea v-model="text" ref="editor" @input="updateText" placeholder="Lorem ipsum ..." rows="12"
      class="text-editor__input"></textarea>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

export default defineComponent({
    name: "TextEditor",
    props: {
        modelValue: String as PropType<string>,
    },
    data() {
        return {
            text: this.modelValue ?? "",
            undoStack: [] as string[],
            redoStack: [] as string[]
        }
    },
    watch: {
        modelValue(newValue: string) {
            this.text = newValue;
        },
    },
    methods: {
        updateText(): void {
            this.undoStack.push(this.text);
            this.$emit("update:modelValue", this.text);
            this.$emit("stack-changed", {
                undoLength: this.undoStack.length,
                redoLength: this.redoStack.length,
            });
        },
        undo(): void {
            if (this.undoStack.length > 0) {
                if (this.undoStack.length > 1) {
                    this.redoStack.push(this.undoStack.pop() ?? "");
                    this.text = this.undoStack[this.undoStack.length - 1];
                } else if (this.undoStack.length === 1) {
                    this.redoStack.push(this.text);
                    this.text = "";
                }
                this.$emit("update:modelValue", this.text);
                this.$emit("stack-changed", {
                    undoLength: this.undoStack.length,
                    redoLength: this.redoStack.length,
                });
            }
        },
        redo(): void {
            if (this.redoStack.length > 0) {
                this.undoStack.push(this.text);
                this.text = this.redoStack.pop() ?? "";
                this.$emit("update:modelValue", this.text);
                this.$emit("stack-changed", {
                    undoLength: this.undoStack.length,
                    redoLength: this.redoStack.length,
                });
            }
        },
        clearText(): void {
            this.undoStack.push(this.text);
            this.text = "";
            this.$emit("update:modelValue", this.text);
            this.$emit("stack-changed", {
                undoLength: this.undoStack.length,
                redoLength: this.redoStack.length,
            });
        },
        handleKeydown(event: KeyboardEvent): void {
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
    },
    mounted() {
        window.addEventListener("keydown", this.handleKeydown);
    },
    beforeUnmount() {
        window.removeEventListener("keydown", this.handleKeydown);
    },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
.text-editor__input {
  width: 100%;
  min-height: 280px;
  padding: 16px;
  border-radius: 16px;
  border: 1px solid #1f262d;
  background: #0b0f14;
  color: #f5f5f5;
  font-size: 1rem;
  font-family: "Georgia", serif;
  resize: vertical;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.35);
}

.text-editor__input:focus {
  outline: none;
  border-color: #0f2dd9;
  box-shadow: 0 0 0 3px rgba(15, 45, 217, 0.18);
}
</style>
