<template>
  <div class="home">
    <div>
      <textarea id="chatContent" v-model="chatContent" placeholder="Insert something in me OwO" cols="50" rows="10" class="form-control" @keyup="update"></textarea>

      <p v-if="errorMessage" class="alert alert-danger" role="alert"> {{ errorMessage }} </p>

      <button type="button" @click="update" class="btn btn-primary" style="margin-top: 4px">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-clockwise" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 0 1 .908-.417A6 6 0 1 1 8 2v1z" />
          <path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z" />
        </svg>
        Refresh
      </button>
      <div class="float-end">total characters: {{ totalcharacter }}</div>
    </div>

    <p></p>

    <div class="table-responsive">
      <table class="table table-striped">
        <tbody>
        <tr v-for="msg in singleMessage">
          <td>{{ msg }}</td>
          <td>
            <button type="button" @click="onCopy(msg)" v-if="msg" class="btn btn-success">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clipboard" viewBox="0 0 16 16">
                <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"></path>
                <path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3zm-3-1A1.5 1.5 0 0 0 5 1.5v1A1.5 1.5 0 0 0 6.5 4h3A1.5 1.5 0 0 0 11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3z"></path>
              </svg>
              Copy
            </button>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
const { clipboard } = require('electron');

export default {
  name: "home",
  data() {
    return {
      chatContent: '',
      contentWordArray: [''],
      singleMessage: [''],
      errorMessage: '',
      totalcharacter: 0
    }
  },
  methods: {
    update() {
      const MSG_CHAR_LIMIT = 197; // character limit per single chat message (in gw2 it's 199, but 197 needed to add ' >' automatically
      let i = 0;                  // place of message
      let j = 0;                  // position of word
      // reset
      this.singleMessage = [''];
      this.contentWordArray = [''];
      this.errorMessage = '';

      this.totalcharacter = this.chatContent.length;
      // generate table if textarea is filled
      if (this.chatContent.length != 0) {
        this.contentWordArray = this.chatContent.split(' ');

        // check if every word is separable
        for (let k = 0; k < this.contentWordArray.length; k++) {
          if (this.contentWordArray[k].length > MSG_CHAR_LIMIT) {
            this.errorMessage = 'At least one word is longer then 197 characters. Try to split it with space.';
            return;
          }
        }

        while (j < this.contentWordArray.length) {
          // check if word fits in message
          if (this.singleMessage[i].length + this.contentWordArray[j].length <= MSG_CHAR_LIMIT) {
            this.singleMessage[i] += this.contentWordArray[j].toString() + ' ';
            //console.log('Msg: ' + this.singleMessage[0])
          } else {
            this.singleMessage[i] += '>';   // finish Message
            this.singleMessage.push('');    // init next message
            i++;
            j--;                            // hold current word to set in next message
          }
          j++;
        }
      }
      //console.log(this.singleMessage)
    },
    onCopy(msg) {
      //console.log("CopyText" + msg);
      clipboard.writeText(msg, 'clipboard')
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
