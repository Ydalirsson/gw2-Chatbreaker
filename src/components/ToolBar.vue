<template>
  <div class="toolbar">
    <div class="toolbar__group">
      <label class="toolbar__label">Separator</label>
      <select v-model.number="localSelected" class="toolbar__select">
        <option disabled value="0">Separator</option>
        <option value="1" selected>&gt; (default)</option>
        <option value="2">+</option>
        <option value="3">-</option>
        <option value="4">~</option>
      </select>
    </div>

    <div class="toolbar__group">
      <label class="toolbar__label">Limit</label>
      <input type="number" min="3" class="toolbar__input" v-model.number="localMaxWordLength"
        title="This field determines the number of characters that can appear in a message. Can be set as required.\n- GW2-Mode: 197\n- Discord-Mode: 1998" />
    </div>

    <div class="toolbar__meta">
      <span>Total characters: {{ totalCharacter }}</span>
    </div>

    <div class="toolbar__actions">
      <button class="btn pill" @click="onUndo" :disabled="undoDisabled" title="Undo (Ctrl+Z / Cmd+Z)">Undo</button>
      <button class="btn pill" @click="onRedo" :disabled="redoDisabled" title="Redo (Ctrl+Y / Cmd+Shift+Z)">Redo</button>
      <button type="button" class="btn pill danger" @click="onClear">Delete</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
export default defineComponent({
  name: "ToolBar",
  props: {
    selected: {type: Number, default: 1},
    maxWordLength: {type: Number, default: 197},
    totalCharacter: {type: Number, default: 0},
    onUndo: {type: Function as PropType<(event: MouseEvent) => void>, required: true},
    onRedo: {type: Function as PropType<(event: MouseEvent) => void>, required: true},
    onClear: {type: Function as PropType<(event: MouseEvent) => void>, required: true },
    undoDisabled: {type: Boolean, required: true},
    redoDisabled: {type: Boolean, required: true}
  },
  data() {
    return {
      localSelected: this.selected,
      localMaxWordLength: this.maxWordLength,
    };
  },
  watch: {
    localSelected(newVal: number) {
      this.$emit("update:selected", newVal);
    },
    localMaxWordLength(newVal: number) {
      this.$emit("update:maxWordLength", newVal);
    },
    selected(newVal: number) {
      this.localSelected = newVal;
    },
    maxWordLength(newVal: number) {
      this.localMaxWordLength = newVal;
    }
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
.toolbar {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr)) auto;
  gap: 12px 16px;
  align-items: center;
}

.toolbar__group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.toolbar__label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #9aa3aa;
}

.toolbar__select,
.toolbar__input {
  height: 38px;
  border-radius: 999px;
  border: 1px solid #1f262d;
  background: #0b0f14;
  color: #f5f5f5;
  padding: 0 14px;
  font-family: "Georgia", serif;
}

.toolbar__meta {
  font-size: 0.9rem;
  color: #9aa3aa;
  font-family: "Georgia", serif;
}

.toolbar__actions {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  border: none;
  background: #0f2dd9;
  color: #f5f5f5;
  padding: 8px 18px;
  border-radius: 999px;
  font-size: 0.9rem;
  font-family: "Georgia", serif;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 10px 20px rgba(8, 12, 20, 0.4);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  box-shadow: none;
}

.btn:hover:not(:disabled) {
  transform: translateY(-1px);
}

.btn.danger {
  background: transparent;
  border: 1px solid #e04b4b;
  color: #e04b4b;
}

@media (max-width: 1100px) {
  .toolbar {
    grid-template-columns: 1fr;
  }

  .toolbar__actions {
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}
</style>
