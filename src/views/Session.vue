<template>
  <v-container v-if="this.$store.state.selectedSession != null" class="my-10">
    <v-overlay :value="this.exportInProgress">
      <v-btn @click="exportInProgress = false">Close</v-btn>
      <SkyIDPublisher v-bind:session="this.$store.state.selectedSession">
      </SkyIDPublisher>
    </v-overlay>

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
                <v-btn icon v-on="on" color="black" v-bind="attrs">
                  <v-icon>{{ isPrivateSession ? "lock" : "lock_open" }}</v-icon>
                </v-btn>
              </template>
              <span>{{ isPrivateSession ? "Private" : "Public" }}</span>
            </v-tooltip>
            <v-btn class="ma-2" outlined color="black" @click="downloadAllLoops"
              >Download all loops</v-btn
            >
            <v-btn class="ma-2" outlined color="black" @click="beginSkyDBExport"
              >Export session to SkyDB</v-btn
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
                <v-tooltip
                  v-for="user in this.$store.state.selectedSession.users"
                  :key="user"
                  top
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-avatar
                      class="avatar"
                      :color="user | getColorForString"
                      size="33"
                      @click="user | goToProfile"
                      v-bind="attrs"
                      v-on="on"
                    >
                    </v-avatar>
                  </template>
                  <span>{{ user }}</span>
                </v-tooltip>
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
          @click="overlay = !overlay"
        >
        </v-img>
        <v-overlay :absolute="absolute" :value="overlay">
          <div>
            <v-btn @click="overlay = false">Close</v-btn>
            <v-img
              :src="this.$store.state.selectedSession.picture"
              class="rounded-lg"
              aspect-ratio="1"
              min-height="50vw"
              min-width="50vw"
              @click="overlay = false"
            ></v-img>
          </div>
        </v-overlay>
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
            :color="tag | getColorForString"
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

.avatar {
  z-index: 1;
}
.avatar:not(:first-child) {
  margin-left: -10px;
}
.avatar:hover {
  z-index: 2;
}
</style>
<script>
import WaveformPlayer from "@/components/WaveformPlayer.vue";
import SkyIDPublisher from "@/components/SkyIDPublisher.vue";
import { getGenericSkynetDownloadLink } from "@/filters/utils";
import { sessionViewFilter } from "@/filters/utils";
import cloudloop from "@/mixins/cloudloop";

export default {
  components: { WaveformPlayer, SkyIDPublisher },
  name: "Session",
  mixins: [cloudloop],
  props: ["on"],
  sockets: {
    message: function(data) {
      console.log("Message from client" + data);
    },
    state_update: function(data) {
      console.log("STATE UPDATE RECEIVED: " + data);
      var session_raw = JSON.parse(data);
      var session_decoded = sessionViewFilter(session_raw);

      this.$store.dispatch("setSelectedSession", { session: session_decoded });
    }
  },
  data() {
    return {
      session: this.selectedSession,
      sessionName: this.$route.params.sessionName,
      exportInProgress: false,
      connected: false,
      showImagePicker: false,
      isPlaying: false,
      isPrivate: this.isPrivateSession,
      absolute: false,
      overlay: false,
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
        let session_raw = data.data.results;
        session_raw.picture = getGenericSkynetDownloadLink(session_raw.picture);
        this.$store.dispatch("setSelectedSession", { session: session_raw });
      })
      .catch(error => {
        console.error(error);
        this.$router.push("/");
      });
  },
  mounted() {
    this.$socket.client.emit("joinSession", {
      username: this.$store.state.loggedInUser.username,
      session_name: this.$route.params.sessionName
    });
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
        if (loop.link.substring(0, 10) !== "reserve://") {
          console.log(`Playing ref:${loop.hash}`);
          return this.$refs[refHandle][0].play;
        }
      });
      console.log({ playFuncs });

      playFuncs.forEach(func => {
        if (func != undefined) {
          func();
        }
      });
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
    },
    beginSkyDBExport() {
      this.exportInProgress = true;
    }
  }
};
</script>
