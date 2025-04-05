<template>
    <div class="text-editor">
        <textarea v-model="text" ref="editor" @input="updateText" placeholder="Insert text here" cols="50" rows="10"
            class="form-control"></textarea>
        <div>
            <button class="btn btn-secondary btn-sm" style="margin-top: 4px" @click="undo"
                :disabled="undoStack.length === 0" title="Undo (Ctrl+Z / Cmd+Z)">Undo</button>
            <button class="btn btn-secondary btn-sm" style="margin-top: 4px" @click="redo"
                :disabled="redoStack.length === 0" title="Redo (Ctrl+Y / Cmd+Shift+Z)">Redo</button>
            <button type="button" class="btn btn-outline-danger btn-sm" style="margin-top: 4px" @click="clearText">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash"
                    viewBox="0 0 16 16">
                    <path
                        d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z" />
                    <path fill-rule="evenodd"
                        d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z" />
                </svg>
                Delete
            </button>
        </div>
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
            redoStack: [] as string[],
        };
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
            }
        },
        redo(): void {
            if (this.redoStack.length > 0) {
                this.undoStack.push(this.text);
                this.text = this.redoStack.pop() ?? "";
                this.$emit("update:modelValue", this.text);
            }
        },
        clearText(): void {
            this.undoStack.push(this.text);
            this.text = "";
            this.$emit("update:modelValue", this.text);
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

<style scoped lang="css"> textarea:focus {
     background-color: #23272a;
     color: #fff;
 }

 input[type="text"],
 textarea {
     background-color: #23272a;
     color: #fff;
 }
</style>
  