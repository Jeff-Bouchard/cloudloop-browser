<template>
  <v-container class="my-10">
    <v-row>
      <v-col cols="4">
        <span class="text-h3 font-weight-medium text-uppercase">
          <v-btn
            fab
            dark
            large
            x-large
            color="black"
            class="mr-4"
            @click="isPlaying = !isPlaying"
          >
            <v-icon dark>
              {{ isPlaying ? "pause" : "play_arrow" }}
            </v-icon>
          </v-btn>
          Example session
        </span>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Session",
  data() {
    return {
      data: require("../../example-data.json"),
      isPlaying: true
    };
  }
};
</script>
