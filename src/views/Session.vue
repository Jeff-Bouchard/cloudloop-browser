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
            @click="handleClick"
          >
            <v-icon dark>
              {{ isPlaying ? "pause" : "play_arrow" }}
            </v-icon>
          </v-btn>
        </div>
        <div class="d-inline-flex">
          <span class="text-h3 font-weight-bold text-uppercase">
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
            <v-btn class="ma-2" outlined color="black" @click="downloadAllLoops"
              >Download all loops</v-btn
            >
          </span>
        </div>
        <div>
          <v-container>
            <v-layout row wrap>
              <v-flex lg2 class="ma-1">
                <v-avatar color="red" size="40" v-on="on" center></v-avatar>
                <div class="text-h5 font-weight-medium text-uppercase">
                  {{ this.$store.state.selectedSession.creator }}
                </div>
              </v-flex>
              <v-flex lg8>
                with
                <v-avatar
                  class="ma-1"
                  :color="randomColor()"
                  v-for="(user, index) in this.$store.state.selectedSession
                    .users"
                  :key="index"
                  v-on="on"
                >
                </v-avatar>
              </v-flex>
            </v-layout>
          </v-container>
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
          :src="this.$store.state.selectedSession.picture"
          class="rounded-lg"
          aspect-ratio="1"
          max-height="400"
          max-width="400"
        >
        </v-img>
        <p class="text-body-1 my-6 cover-text">
          {{ this.$store.state.selectedSession.blurb }}
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
      <v-spacer></v-spacer>
      <v-col cols="12" lg="7">
        <div
          v-for="loop in this.$store.state.selectedSession.slots"
          :key="loop.hash"
        >
          <WaveformPlayer :loop="loop" :ref="'ref-' + loop.hash" />
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
import WaveformPlayer from "@/components/WaveformPlayer.vue";
import { getGenericSkynetDownloadLink } from "@/filters/utils";
import cloudloop from "@/mixins/cloudloop";

export default {
  name: "Session",
  components: { WaveformPlayer },
  mixins: [cloudloop],
  props: ["on"],
  data() {
    return {
      session: this.selectedSession,
      sessionName: this.$route.params.sessionName ?? null,
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
    // return to home if no sessionName was provided
    // might want to default to creating a new session instead
    if (!this.sessionName) return this.$router.push("/");

    this.fetchSession(this.sessionName)
      .then(data => {
        console.log(`session ${this.sessionName}:`);
        console.log(data);
        let session_raw = data.data.results;
        session_raw.picture = getGenericSkynetDownloadLink(session_raw.picture);
        session_raw.private = session_raw.private === "true";
        this.$store.dispatch("setSelectedSession", { session: session_raw });
      })
      .catch(error => {
        console.error(error);
        this.$router.push("/");
      });

    // const fetchOptions = {
    //   credentials: "include",
    //   headers: {
    //     "Content-Type": "application/json",
    //     Authorization: `JWT ${window.localStorage.getItem("JWT")}`
    //   }
    // };

    // fetch(
    //   "https://dev.cloudloop.io/session?session_name=" + this.sessionName,
    //   fetchOptions
    // ).then(response => {
    //   if (response.ok) {
    //     response.json().then(jsonData => {
    //       var session_raw = jsonData.data.results;
    //       session_raw.picture = getGenericSkynetDownloadLink(
    //         session_raw.picture
    //       );
    //       session_raw.private = session_raw.private === "true";

    //       this.$store
    //         .dispatch("setSelectedSession", { session: session_raw })
    //         .then(resolve(this.session));
    //     });
    //   } else {
    //     console.error(response.status);
    //     reject(response.json().message);
    //   }
    // });
  },

  methods: {
    randomColor() {
      return this.colors[Math.floor(Math.random() * this.colors.length)];
    },
    handleClick() {
      if (this.isPlaying) this.pauseAllLoops();
      else this.playAllLoops();
    },
    playAllLoops() {
      const playFuncs = Object.values(
        this.$store.state.selectedSession.slots
      ).map(loop => {
        const refHandle = `ref-${loop.hash}`;
        return this.$refs[refHandle][0].play;
      });
      console.log({ playFuncs });

      playFuncs.forEach(func => func());
      this.isPlaying = true;
    },
    pauseAllLoops() {
      const pauseFuncs = Object.values(
        this.$store.state.selectedSession.slots
      ).map(loop => {
        const refHandle = `ref-${loop.hash}`;
        return this.$refs[refHandle][0].pause;
      });

      pauseFuncs.forEach(func => func());
      this.isPlaying = false;
    },
    downloadAllLoops() {
      location.href =
        "https://dev.cloudloop.io/download/library?session_name=" +
        this.sessionName;
    }
  }
};
</script>
