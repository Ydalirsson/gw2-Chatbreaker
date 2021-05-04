<template>
  <div class="hello">
    <br>
    <textarea v-model="chatContent" placeholder="Insert something in me OwO" cols="60" rows="10" class="area" @keyup="update"></textarea>
    <p> total input charrrrrrrrs: {{ totalcharacter }}</p>
    <button type="button" @click="update">Aktualisieren</button>
    <table id class="display table" width="100%">
      <tbody>
      <tr v-for="(msg, index) in singleMessage" :key="index">
        <td>{{ msg }}</td>
        <td><button type="button" @click="onCopy(msg)">Copy to Clipboard</button></td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
const {clipboard} = require('electron');

export default {
  name: "hello",
  data() {
    return {
      chatContent: '',
      contentWordArray: [''],
      singleMessage: [''],
      totalcharacter: 0
      }
    },
  methods: {
    countChars() {
      this.totalcharacter = this.chatContent.length;
      // add >
      if (this.totalcharacter % 197 == 0) {
        this.contentWordArray = this.chatContent.split('');
        this.contentWordArray.push(' ');
        this.contentWordArray.push('>');
        console.log(this.contentWordArray.toString());
      }
      //breaking message
    },
    update() {
      const MSGLIMIT = 198;
      let i = 0;
      let j = 0;
      //reset
      this.singleMessage = [''];
      this.contentWordArray = [''];

      this.totalcharacter = this.chatContent.length;
      this.contentWordArray = this.chatContent.split(' ');

      while (j < this.contentWordArray.length) {
      if (this.singleMessage[i].length + this.contentWordArray[j].length <= MSGLIMIT) {
        this.singleMessage[i] += this.contentWordArray[j].toString() + ' ';
        console.log('Msg: ' + this.singleMessage[0])
        } else {
           // finish Message
           this.singleMessage[i] += '>';
          // init next message
          this.singleMessage.push('');
          i++;
          j--;
      }
      j++;
      }
      console.log(this.singleMessage)

    },
    onCopy(msg) {
      console.log("CopyText" + msg);
      clipboard.writeText(msg, 'clipboard')
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
  .area {
    height: 50%;
    width: 50%
  }
</style>
