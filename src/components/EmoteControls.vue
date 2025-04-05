<template>
  <div>
    <button type="button" class="btn btn-primary" style="margin-top: 4px" @click="insertTextAtCursor(' /e ')">Start
      emote</button>
    <button type="button" class="btn btn-primary" style="margin-top: 4px" @click="insertTextAtCursor(' ## ')">End
      emote</button>
    <div id="emoteListID" class="list-group" @click="changeEmoteList" v-if="listCollapsed">
      <span class="tooltiptext">Click to collapse</span>
      <li v-for="(emote, index) in emoteList" :key="index" class="list-group-item py-0"
        @click.stop="handleInsert(' ' + emote + ' ')">{{ emote }}</li>
    </div>
    <div id="emoteID" class="list-group" @click="changeEmoteList" v-else>
      <li class="list-group-item">List of emotes</li>
      <span class="tooltiptext">Click to expand</span>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'EmoteControls',
  props: {
    insertTextAtCursor: {
      type: Function,
      required: true,
    }
  },
  data() {
    return {
      listCollapsed: false as boolean,
      emoteList: [
        "/beckon",
        "/bless",
        "/bow",
        "/cheer",
        "/cower",
        "/crossarms",
        "/cry",
        "/dance",
        "/facepalm",
        "/upset",
        "/geargrind",
        "/heroic",
        "/hiss",
        "/kneel",
        "/laugh",
        "/magicjuggle",
        "/no",
        "/paper",
        "/playdead",
        "/point",
        "/ponder",
        "/possessed",
        "/rank",
        "/readbook",
        "/rock",
        "/rockout",
        "/sad",
        "/salute",
        "/scissors",
        "/scis",
        "/serve",
        "/shiver",
        "/shiverplus",
        "/shrug",
        "/shuffle",
        "/sipcoffee",
        "/sit",
        "/sleep",
        "/step",
        "/stretch",
        "/surprised",
        "/talk",
        "/thanks",
        "/thank",
        "/thx",
        "/ty",
        "/threaten",
        "/wave",
        "/yes",
        "/e",
        "/em",
        "/emote",
        "/me"
      ]
    };
  },
  methods: {
    changeEmoteList(): void {
      this.listCollapsed = !this.listCollapsed;
    },
    handleInsert(text: string): void {
      this.insertTextAtCursor(text);
    },
  }
});
</script>


<style lang="css">
#emoteID .tooltiptext,
#emoteListID .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: static;
  z-index: 1;
  top: 20px;
  /* Beispiel: Verschiebung um 20px nach unten */
  left: 0;
  /* Beispiel: Tooltip linksbündig */
}

#emoteID:hover .tooltiptext,
#emoteListID:hover .tooltiptext,
#emoteID.active .tooltiptext,
#emoteListID.active .tooltiptext {
  visibility: visible;
}

#emoteID,
#emoteListID {
  font-size: 10pt;
}

#emoteListID {
  position: relative;
  top: -25px;
}
</style>