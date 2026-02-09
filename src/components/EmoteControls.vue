<template>
  <div class="emotes">
    <div class="emotes__actions">
      <button type="button" class="pill" @click="handleInsert(' /e ')">Start emote</button>
      <button type="button" class="pill" @click="handleInsert(' ## ')">End emote</button>
    </div>

    <input class="emotes__search" type="search" placeholder="Search for emote ..." v-model="emoteFilter" />

    <div class="emotes__grid">
      <button v-for="(emote, index) in filteredEmotes" :key="index" class="emotes__item"
        @click="handleInsert(' ' + emote + ' ')">
        {{ emote }}
      </button>
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
      emoteFilter: "" as string,
      emoteList: [
        "/beckon",
        "/bless",
        "/bloodstoneboogie",
        "/boogie",
        "/bow",
        "/breakdance",
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
        "/petalthrow",
        "/playdead",
        "/point",
        "/ponder",
        "/PoseCover",
        "/PoseHigh",
        "/PoseHigh",
        "/PoseTwist",
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
        "/unleash",
        "/wave",
        "/yes",
        "/e",
        "/em",
        "/emote",
        "/me"
      ]
    };
  },
  computed: {
    filteredEmotes(): string[] {
      const query = this.emoteFilter.toLowerCase().trim();
      if (!query) return this.emoteList;
      return this.emoteList.filter((emote) => emote.toLowerCase().includes(query));
    }
  },
  methods: {
    handleInsert(text: string): void {
      this.insertTextAtCursor(text);
    },
  }
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
.emotes {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.emotes__actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.pill {
  border: none;
  background: #0f2dd9;
  color: #f5f5f5;
  padding: 8px 18px;
  border-radius: 999px;
  font-family: "Georgia", serif;
  cursor: pointer;
  box-shadow: 0 10px 20px rgba(8, 12, 20, 0.4);
}

.emotes__search {
  height: 40px;
  border-radius: 999px;
  border: 1px solid #1f262d;
  background: #0b0f14;
  color: #f5f5f5;
  padding: 0 16px;
  font-family: "Georgia", serif;
}

.emotes__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}

.emotes__item {
  border: 1px solid #1f262d;
  border-radius: 10px;
  background: #273038;
  color: #e6e6e6;
  padding: 8px;
  font-size: 0.8rem;
  font-family: "Georgia", serif;
  text-align: left;
  cursor: pointer;
}

@media (max-width: 1100px) {
  .emotes__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
