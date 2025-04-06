<template>
  <ul class="controlBar">
    <EmoteControls :insertTextAtCursor="insertTextAtCursor" />
    <li>
      <select v-model.number="localSelected" class="form-select form-select-sm"
        style="margin-top: 4px; width: 110px; height: 38px">
        <option disabled value="0">Separator</option>
        <option value="1" selected>> (default)</option>
        <option value="2">+</option>
        <option value="3">-</option>
        <option value="4">~</option>
      </select>
    </li>

    <li>
      <input type="number" placeholder="Limit" value="197" min="3" class="form-control form-control-sm"
        style="margin-top: 4px; width: 110px; height: 38px" data-toggle="tooltip" data-placement="bottom" title="This field determines the number of characters that can appear in a message. Can be set as required.
            - GW2-Mode: 197
            - Discord-Mode: 1998" v-model.number="localMaxWordLength">
    </li>

    <li>
      <span class="badge bg-secondary">total characters: {{ totalCharacter }}</span>
    </li>

    <div>
      <button class="btn btn-secondary btn-sm" style="margin-top: 4px" @click="onUndo" :disabled="undoDisabled"
        title="Undo (Ctrl+Z / Cmd+Z)">Undo</button>
      <button class="btn btn-secondary btn-sm" style="margin-top: 4px" @click="onRedo" :disabled="redoDisabled"
        title="Redo (Ctrl+Y / Cmd+Shift+Z)">Redo</button>
      <button type="button" class="btn btn-outline-danger btn-sm" style="margin-top: 4px" @click="onClear">
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

  </ul>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import EmoteControls from "./EmoteControls.vue";

export default defineComponent({
  name: "ToolBar",
  components: {
    EmoteControls
  },
  props: {
    selected: {type: Number, default: 1},
    maxWordLength: {type: Number, default: 197},
    totalCharacter: {type: Number, default: 0},
    onUndo: {type: Function as PropType<(event: MouseEvent) => void>, required: true},
    onRedo: {type: Function as PropType<(event: MouseEvent) => void>, required: true},
    onClear: {type: Function as PropType<(event: MouseEvent) => void>, required: true },
    undoDisabled: {type: Boolean, required: true},
    redoDisabled: {type: Boolean, required: true},
    insertTextAtCursor: {type: Function as PropType<(text: string) => void>, required: true}
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
.controlBar {
  display: flex;
  justify-content: space-between;
  list-style: none;
  padding-left: 0;
}

select {
  background-color: #375a7f;
  color: #fff;
}
</style>