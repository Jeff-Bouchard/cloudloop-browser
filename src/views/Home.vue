<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4">
        <h1 v-if="!loggedInUser" class="display-2 font-weight-bold mb-3">
          Welcome to cloudloop
        </h1>
        <h1 v-else class="display-2 font-weight-bold mb-3">
          Welcome back, {{ loggedInUser.username }}
        </h1>

        <p class="subheading font-weight-regular">
          CloudLoop is a collaborative loop station and audio library.<br />
          Check out the sessions below, or create your own by dragging and
          dropping some audio!<br />
        </p>
      </v-col>
      <v-col cols="12">
        <SessionCard
          class="mb-4 col-md-6 offset-md-3"
          v-for="(sessionHeader, index) in sessionHeaders"
          :key="index"
          :sessionHeader="sessionHeader"
        />
      </v-col>

      <v-col class="mb-5" cols="12">
        <h2 class="headline font-weight-bold mb-3">What's next?</h2>

        <v-row justify="center">
          <router-link
            v-for="(next, i) in whatsNext"
            :key="i"
            :to="next.to"
            class="subheading mx-3"
          >
            {{ next.text }}
          </router-link>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import SessionCard from "@/components/SessionCard.vue";
import cloudloop from "@/mixins/cloudloop";

export default {
  name: "Home",
  mixins: [cloudloop],
  components: { SessionCard },
  data: () => ({
    sessionHeaders: [],
    whatsNext: [
      {
        text: "My Sessions",
        to: "sessions"
      }
    ]
  }),

  computed: {
    loggedInUser() {
      return this.$store.state.loggedInUser;
    }
  },

  mounted() {
    if (this.loggedInUser) {
      this.fetchPublicSessionHeaders()
        .then(data => {
          this.sessionHeaders = data.data.results.splice(0, 50);
        })
        .catch(console.error);
    }
  }
};
</script>
