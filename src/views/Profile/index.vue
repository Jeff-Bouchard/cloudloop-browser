<template>
  <v-container v-if="user != null" class="my-10">
    <v-row class="mb-10">
      <v-col cols="12" lg="3">
        <ProfileInfo />
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
import ProfileInfo from "./ProfileInfo.vue";
import Sessions from "./Sessions.vue";
import Followers from "./Followers.vue";

export default {
  name: "Profile",
  components: { ProfileInfo, Sessions, Followers },
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
      const user = this.$store.state.selectedProfile;
      console.log({user});
      return user;
    }
  },

  beforeMount: function() {
    this.$store.dispatch("fetchUserProfile", this.userName);
  }
};
</script>
