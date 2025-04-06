<template>
    <div class="text-editor">
        <textarea v-model="text" ref="editor" @input="updateText" placeholder="Insert text here" cols="50" rows="10"
            class="form-control"></textarea>
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
textarea:focus {
    background-color: #23272a;
    color: #fff;
}

input[type="text"],
textarea {
    background-color: #23272a;
    color: #fff;
}
</style>