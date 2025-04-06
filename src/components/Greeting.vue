<template>
    <div class="greeting">
      <p style="font-size: 10pt">
        Hello, today is {{ currentMouvDate() }}, {{ currentElonDate() }},
        {{ currentCantDate() }}
      </p>
    </div>
</template>
  
  <script lang="ts">
  export default {
    methods: {
      currentMouvDate(): string {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(
        dateNow.getFullYear(),
        0,
        1,
        23,
        59,
        59,
        999
      );
      let dayOfYear =
        Math.floor(dateNow.getTime() - currentYear.getTime()) /
        1000 /
        60 /
        60 /
        24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = "";
      let mouveCalenderDay = 0;
      if (1 <= dayOfYear && dayOfYear <= 90) {
        season = "Zephyr";
        mouveCalenderDay = dayOfYear;
      } else if (91 <= dayOfYear && dayOfYear <= 180) {
        season = "Phoenix";
        mouveCalenderDay = dayOfYear - 90;
      } else if (181 <= dayOfYear && dayOfYear <= 270) {
        season = "Scion";
        mouveCalenderDay = dayOfYear - 180;
      } else if (271 <= dayOfYear && dayOfYear <= 366) {
        season = "Colossus";
        mouveCalenderDay = dayOfYear - 270;
      }
      return (
        mouveCalenderDay +
        " " +
        season +
        " " +
        (dateNow.getFullYear() - 687) +
        " A.E."
      );
    },
    currentElonDate(): string {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(
        dateNow.getFullYear(),
        0,
        1,
        23,
        59,
        59,
        999
      );
      let dayOfYear =
        Math.floor(dateNow.getTime() - currentYear.getTime()) /
        1000 /
        60 /
        60 /
        24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = "";
      let mouveCalenderDay = 0;
      if (1 <= dayOfYear && dayOfYear <= 90) {
        season = "Zephyr";
        mouveCalenderDay = dayOfYear;
      } else if (91 <= dayOfYear && dayOfYear <= 180) {
        season = "Phoenix";
        mouveCalenderDay = dayOfYear - 90;
      } else if (181 <= dayOfYear && dayOfYear <= 270) {
        season = "Scion";
        mouveCalenderDay = dayOfYear - 180;
      } else if (271 <= dayOfYear && dayOfYear <= 366) {
        season = "Colossus";
        mouveCalenderDay = dayOfYear - 270;
      }
      return (
        mouveCalenderDay +
        " " +
        season +
        " " +
        (dateNow.getFullYear() - 687 + 200) +
        " D.Z."
      );
    },
    currentCantDate(): string {
      const dateNow = new Date(Date.now());
      const currentYear = new Date(
        dateNow.getFullYear(),
        0,
        1,
        23,
        59,
        59,
        999
      );
      let dayOfYear =
        Math.floor(dateNow.getTime() - currentYear.getTime()) /
        1000 /
        60 /
        60 /
        24;
      dayOfYear = Math.floor(dayOfYear) + 2;

      let season = "";
      let mouveCalenderDay = dateNow.getDate();

      switch (dateNow.getMonth()) {
        case 0:
          season = "Changhai";
          break;
        case 1:
          season = "Zhoyo";
          break;
        case 2:
          season = "Nongkam";
          break;
        case 3:
          season = "Zalfawn";
          break;
        case 4:
          season = "Saita";
          break;
        case 5:
          season = "Mikan";
          break;
        case 6:
          season = "Nemnai";
          break;
        case 7:
          season = "Beibacah";
          break;
        case 8:
          season = "Suzhen";
          break;
        case 9:
          season = "Yundinfang";
          break;
        case 10:
          season = "Songtahn";
          break;
        case 11:
          season = "Kainengtah";
          break;

        default:
          season = "";
          break;
      }

      return (
        mouveCalenderDay +
        " " +
        season +
        " " +
        (dateNow.getFullYear() - 687 + 510) +
        " C.K."
      );
    },

    }
  };
  </script>
  
<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="css">
</style>