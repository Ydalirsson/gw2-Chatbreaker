<template>
  <div class="home">
    <div>
      <p style="font-size: 10pt">Hello, today is {{currentDate()}}!</p>
    </div>

    <div>
      <textarea id="chatContent" v-model="chatContent" ref="chatEdit" placeholder="Insert something in me OwO" cols="50" rows="10" class="form-control" @keyup="update"></textarea>

      <p v-if="errorMessage" class="alert alert-danger" role="alert"> {{ errorMessage }} </p>

      <button type="button" class="btn btn-primary float-start" style="margin-top: 4px" @click="delete">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
          <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
          <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
        </svg>
        Delete
      </button>

      <select class="form-select form-select-sm" style="margin-top: 4px; width: 110px; height: 38px;"
              v-model="selected" @change="update">
        <option disabled value="0">Separator</option>
        <option value="1">> (default)</option>
        <option value="2">+</option>
        <option value="3">-</option>
        <option value="4">~</option>
      </select>

      <div class="float-end">total characters: {{ totalCharacter }}</div>
    </div>

    <p></p><br>

    <div class="table-responsive">
      <table class="table table-dark table-striped">
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

<script lang="ts">
import { defineComponent } from "vue";
import { clipboard } from "electron";

export default defineComponent({
  name: "home",
  data() {
    return {
      chatContent: '' as string,
      contentWordArray: [''] as Array<string>,
      singleMessage: [''] as Array<string>,
      errorMessage: '' as string,
      totalCharacter: 0 as number,
      selected: '0'
    }
  },
  methods: {
    currentDate() {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(dateNow.getFullYear(), 0, 1, 23,59,59,999);
      let dayOfYear = Math.floor(dateNow.getTime() - currentYear.getTime()) /1000/60/60/24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = '';
      let mouveCalenderDay = 0;
      if (1 <= dayOfYear && dayOfYear <= 90) {
        season = 'Zephyr';
        mouveCalenderDay = dayOfYear;
      } else if (91 <= dayOfYear && dayOfYear <= 180) {
        season = 'Phoenix';
        mouveCalenderDay = dayOfYear - 90;
      } else if (181 <= dayOfYear && dayOfYear <= 270) {
        season = 'Scion';
        mouveCalenderDay = dayOfYear - 180;
      } else if (271 <= dayOfYear && dayOfYear <= 366) {
        season = 'Colossus';
        mouveCalenderDay = dayOfYear - 270;
      }
      return mouveCalenderDay + ' ' + season + ' ' + (dateNow.getFullYear()-687) + ' A.E.';
      },
    delete(): void {
      this.chatContent = '';
      this.singleMessage = [''];
      this.contentWordArray = [''];
      this.errorMessage = '';

      this.totalCharacter = this.chatContent.length;
      (this.$refs.chatEdit as HTMLElement).focus();
    },
    update() : void {
      const MSG_CHAR_LIMIT = 197; // character limit per single chat message (in gw2 it's 199, but 197 needed to add ' >' automatically
      let i = 0;                  // place of message
      let j = 0;                  // position of word
      let separatorChar = '>';
      // reset
      this.singleMessage = [''];
      this.contentWordArray = [''];
      this.errorMessage = '';

      // set select separation char
      if (this.selected == '1')
        separatorChar = '>';
      else if (this.selected == '2')
        separatorChar = '+';
      else if (this.selected == '3')
        separatorChar = '-';
      else if (this.selected == '4')
        separatorChar = '~';
      else separatorChar = '>';

      this.totalCharacter = this.chatContent.length;
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
            this.singleMessage[i] += separatorChar;   // finish Message
            this.singleMessage.push('');    // init next message
            i++;
            j--;                            // hold current word to set in next message
          }
          j++;
        }
      }
      //console.log(this.singleMessage)
    },
    onCopy(msg: string) : void {
      //console.log("CopyText" + msg);
      clipboard.writeText(msg, 'clipboard')
    },
  }
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
  textarea:focus {
    background-color : #23272a ;
    color: #fff;
  }
  input[type="text"], textarea {
    background-color : #23272a ;
    color: #fff;
  }
  select {
    background-color : #375a7f ;
    color: #fff;
  }
</style>
