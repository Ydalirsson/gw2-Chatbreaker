<template>
  <div class="toolbar d-flex align-items-center justify-content-between mb-2">
    <!-- Separator Auswahl -->
    <div class="d-flex align-items-center">
      <select v-model.number="localSelected" class="form-select form-select-sm"
        style="margin-top: 4px; width: 110px; height: 38px" @change="seperatorChange">
        <option disabled value="0">Separator</option>
        <option value="1" selected>> (default)</option>
        <option value="2">+</option>
        <option value="3">-</option>
        <option value="4">~</option>
      </select>
    </div>

    <!-- Maximale Wortlänge 
    <div class="d-flex align-items-center">
      <label for="maxWordLength" class="me-2">Max Wortlänge:</label>
      <input id="maxWordLength" type="number" v-model.number="localMaxWordLength" class="form-control form-control-sm"
        style="width: 80px" />
    </div>-->

    <div class="d-flex align-items-center">
      <input type="number" placeholder="Limit" value="197" min="3" class="form-control form-control-sm"
        style="margin-top: 4px; width: 110px; height: 38px" data-toggle="tooltip" data-placement="bottom" title="This field determines the number of characters that can appear in a message. Can be set as required.
            - GW2-Mode: 197
            - Discord-Mode: 1998" v-model.number="localMaxWordLength">
    </div>

    <!-- Zeichenanzahl Anzeige -->
    <div>
      <span class="badge bg-secondary">Zeichen: {{ totalCharacter }}</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "Toolbar",
  props: {
    // Der ausgewählte Separator, via v-model:selected
    selected: {
      type: Number,
      default: 1,
    },
    // Das maximale Wortlängen-Limit, via v-model:maxWordLength
    maxWordLength: {
      type: Number,
      default: 197,
    },
    // Die aktuelle Zeichenanzahl (wird vom Parent berechnet)
    totalCharacter: {
      type: Number,
      default: 0,
    },
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

<style scoped>
.toolbar {
  padding: 8px;
  border-bottom: 1px solid #ccc;
}

.toolbar {
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