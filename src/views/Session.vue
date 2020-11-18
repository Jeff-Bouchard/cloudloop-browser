<template>
  <v-container class="my-10">
    <v-row class="mb-10">
      <v-col cols="12">
        <div class="d-inline-flex">
          <v-btn
            fab
            dark
            large
            x-large
            class="mr-4"
            color="black"
            @click="isPlaying = !isPlaying"
          >
            <v-icon dark>
              {{ isPlaying ? "pause" : "play_arrow" }}
            </v-icon>
          </v-btn>
        </div>
        <div class="d-inline-flex">
          <span class="text-h3 font-weight-medium text-uppercase">
            {{ session.name }}
            <v-tooltip bottom close-delay="500">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  v-on="on"
                  color="black"
                  v-bind="attrs"
                  @click="isPrivate = !isPrivate"
                >
                  <v-icon>{{ isPrivate ? "lock" : "lock_open" }}</v-icon>
                </v-btn>
              </template>
              <span>{{ isPrivate ? "Private" : "Public" }}</span>
            </v-tooltip>
          </span>
        </div>

        <!-- This inline flex thing doesn't really work how I wanted -->
        <!-- need to find a way to bring that avatar(s) below the title -->

        <!-- <div class="d-inline-flex">
          <v-avatar color="teal" size="48">
            <span class="white--text headline">48</span>
          </v-avatar>
        </div> -->
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="4">
        <v-img
          src="https://skyportal.xyz/HAClCALSAo5HaaELUam8iSp6fAHMik5Oy6sXtAUNIUE8_Q"
          class="rounded-lg"
          aspect-ratio="1"
          max-height="400"
          max-width="400"
        >
        </v-img>
        <p class="text-body-1 my-6 cover-text">
          Lorem ipsum dolor, sit amet consectetur adipisicing elit. Harum ea
          corporis voluptate iure, quaerat excepturi fugiat sit, alias fugit
          optio blanditiis, laborum autem magnam iste delectus modi at obcaecati
          a.
        </p>
        <div>
          <v-chip
            dark
            close
            class="ma-2"
            v-for="(tag, index) in sessionTags"
            :key="index"
            @click:close="removeTag()"
            :color="randomColor()"
          >
            {{ tag }}
          </v-chip>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.cover-text {
  max-width: 400px;
}
</style>

<script>
export default {
  name: "Session",
  data() {
    return {
      session: require("../../example-data.json"),
      isPlaying: true,
      isPrivate: true,
      sessionTags: ["Drums", "Vocals", "Keys", "Other"],
      colors: ["red", "orange", "amber", "green", "blue", "purple", "blue-grey"]
    };
  },

  methods: {
    randomColor() {
      return this.colors[Math.floor(Math.random() * this.colors.length)];
    }
  }
};
</script>
