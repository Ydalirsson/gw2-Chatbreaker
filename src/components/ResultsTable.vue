<template>
    <div class="results">
        <div class="results__row" v-for="msg in singleMessages" :key="msg.text">
            <span class="results__text">{{ msg.text }}</span>
            <button type="button" @click="onCopy(msg)" v-if="msg.text" class="results__copy">Copy</button>
            <span class="results__check" v-if="msg.copied">✓</span>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    name: "ResultsTable",
    props: {
        singleMessages: {
            type: Array as () => Array<{ text: string; copied: boolean }>,
            required: true,
        }
    },
    methods: {
        onCopy(msg: { text: string, copied: boolean }): void {
            //console.log("CopyText" + msg);
            navigator.clipboard.writeText(msg.text);
            msg.copied = true;
        }
    }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
.results {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.results__row {
    display: grid;
    grid-template-columns: 1fr auto auto;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 12px;
    background: #151b20;
    border: 1px solid #1f262d;
}

.results__text {
    color: #e4e9ee;
    font-size: 0.95rem;
    font-family: "Georgia", serif;
}

.results__copy {
    border: 1px solid #0f2dd9;
    color: #e4e9ee;
    background: transparent;
    border-radius: 999px;
    padding: 6px 14px;
    font-family: "Georgia", serif;
    cursor: pointer;
}

.results__check {
    color: #67dd8c;
    font-size: 1.2rem;
}
</style>
