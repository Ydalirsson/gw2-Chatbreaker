<template>
    <div class="table-responsive">
        <table class="table table-dark table-striped">
            <tbody>
                <tr v-for="msg in singleMessages" v-bind:key="msg.text">
                    <td>{{ msg.text }}</td>
                    <td>
                        <button type="button" @click="onCopy(msg)" v-if="msg.text" class="btn btn-outline-info">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                class="bi bi-clipboard" viewBox="0 0 16 16">
                                <path
                                    d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z">
                                </path>
                                <path
                                    d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z">
                                </path>
                            </svg>
                            Copy
                        </button>
                    </td>
                    <td v-if="msg.copied">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="green" class="bi bi-check"
                            viewBox="0 0 16 16">
                            <path
                                d="M10.97 4.97a.75.75 0 0 1 1.07 1.05l-3.99 4.99a.75.75 0 0 1-1.08.02L4.324 8.384a.75.75 0 1 1 1.06-1.06l2.094 2.093 3.473-4.425a.267.267 0 0 1 .02-.022z" />
                        </svg>
                    </td>
                </tr>
            </tbody>
        </table>
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
    data() {
        return {
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
</style>