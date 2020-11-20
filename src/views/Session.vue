<template>
  <v-container v-if="this.$store.state.selectedSession != null" class="my-10">
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
            {{ sessionName }}
            <v-tooltip bottom close-delay="500">
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  v-on="on"
                  color="black"
                  v-bind="attrs"
                  @click="isPrivate = !isPrivate"
                >
                  <v-icon>{{ isPrivateSession ? "lock" : "lock_open" }}</v-icon>
                </v-btn>
              </template>
              <span>{{ isPrivateSession ? "Private" : "Public" }}</span>
            </v-tooltip>
          </span>
        </div>
        <div>
          <span class="text-h5 font-weight-medium text-uppercase">
            {{this.$store.state.selectedSession.creator}}
          </span>
          <v-avatar color="red" size="40" v-on="on"></v-avatar>
          with
          <v-avatar
              :color="randomColor()"
              v-for="(user, index) in this.$store.state.selectedSession.users"
              :key="index"
              v-on="on"></v-avatar>
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
          :src= "this.$store.state.selectedSession.picture"
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

import {getDownloadLink} from "@/filters/utils";

export default {
  name: "Session",
  data() {
    return {
      session: this.selectedSession,
      sessionName: this.$route.params.sessionName,
      isPlaying: false,
      isPrivate: this.isPrivateSession,
      sessionTags: ["Drums", "Vocals", "Keys", "Other"],
      colors: ["red", "orange", "amber", "green", "blue", "purple", "blue-grey"]
    };
  },

  computed: {
    loggedInUser() {
      return this.$store.state.loggedInUser;
    },
    selectedSession() {
      return this.$store.state.selectedSession;
    },
    isPrivateSession() {
      return this.$store.state.selectedSession.private;
    }
  },

  beforeMount: function() {
    return new Promise((resolve, reject) => {
      const fetchOptions = {
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Authorization: `JWT ${window.localStorage.getItem("JWT")}`
        }
      };

      fetch(
          "https://dev.cloudloop.io/session?session_name=" + this.sessionName,
          fetchOptions
      ).then(response => {
        if (response.ok) {
          response.json().then(jsonData => {
            console.log(jsonData);
            var session_raw = jsonData.data.results;
            session_raw.picture = getDownloadLink(session_raw.picture);
            session_raw.private = session_raw.private === "true";

            this.$store
              .dispatch("setSelectedSession", { session: session_raw })
              .then(resolve(this.session));
          });
        } else {
          console.error(response.status);
          reject(response.json().message);
        }
      });
    });
  },

  methods: {
    randomColor() {
      return this.colors[Math.floor(Math.random() * this.colors.length)];
    }
  }
};
</script>
