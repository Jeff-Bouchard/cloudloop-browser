<template>
  <v-container v-if="user != null" class="my-10">
    <v-row class="mb-10">
      <v-col cols="12" lg="3">
        <v-row justify="center">
          <v-avatar size="200">
            <img :src="profilePicture" :alt="user.username" />
          </v-avatar>
        </v-row>
        <v-row justify="center">
          <h3>{{this.$store.state.selectedProfile.username}}</h3>
        </v-row>
        <p class="text-body-1 my-6 cover-text">
          {{this.$store.state.selectedProfile.bio}}
        </p>
        <div>
          <!-- <v-chip
              dark
              close
              class="ma-2"
              v-for="(tag, index) in sessionTags"
              :key="index"
              @click:close="removeTag()"
              :color="randomColor()"
            >
              {{ tag }}
            </v-chip> -->
        </div>
      </v-col>
      <v-spacer> </v-spacer>
      <v-col cols="12" lg="8">
        <v-tabs v-model="tab" grow>
          <v-tab>Sessions</v-tab>
          <v-tab>Favorites</v-tab>
          <v-tab>Followers</v-tab>
          <v-tab>Following</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item>
            <Sessions />
          </v-tab-item>
          <v-tab-item>Favorites</v-tab-item>
          <v-tab-item><Followers :followers="user.friends"/></v-tab-item>
          <v-tab-item><Followers :followers="user.friends"/></v-tab-item>
        </v-tabs-items>
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
import { getGenericSkynetDownloadLink } from "@/filters/utils";
import Sessions from "./Sessions.vue";
import Followers from "./Followers.vue";

export default {
  name: "Profile",
  components: { Sessions, Followers },
  data() {
    return {
      tab: null,
      session: this.selectedSession,
      userName: this.$route.params.userName,
      isPlaying: false,
      isPrivate: this.isPrivateSession,
      sessionTags: ["Drums", "Vocals", "Keys", "Other"],
      colors: ["red", "orange", "amber", "green", "blue", "purple", "blue-grey"]
    };
  },

  watch: {
    $route() {
      this.$store.dispatch("fetchUserProfile", this.userName);
    }
  },
  computed: {
    profilePicture() {
      return getGenericSkynetDownloadLink(
        this.$store.state.selectedProfile.picture_link
      );
    },
    loggedInUser() {
      return this.$store.state.loggedInUser;
    },
    user() {
      return this.$store.state.selectedProfile;
    }
  },

  beforeMount: function() {
    this.$store.dispatch("fetchUserProfile", this.userName);
  }
};
</script>
