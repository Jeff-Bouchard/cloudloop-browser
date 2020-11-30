<template>
  <v-container>
    <v-row justify="center">
      <v-avatar size="200">
        <img :src="profilePicture" :alt="user.username" />
      </v-avatar>
    </v-row>
    <v-row justify="center">
      <h1 class="headline username">
        {{ user.username.toUpperCase() }}
      </h1>
    </v-row>
    <v-row justify="center">
      <v-col cols="12" lg="6">
        <p class="friends">
          {{ Object.keys(user.friends).length }} Following
        </p>
      </v-col>
      <v-col cols="12" lg="6">
        <p class="friends">
          {{ Object.keys(user.friends).length }} Followers
        </p>
      </v-col>
    </v-row>
    <v-hover v-slot="{ hover }">
      <div class="bio-container">
        <v-icon v-if="hover" class="edit-icon">
          mdi-pencil-circle
        </v-icon>
      <v-textarea @blur="handleBioUpdate" id="bio-text" style="resize: none;" solo flat v-model="user.bio">
        {{ user.bio }}
      </v-textarea>
      </div>
    </v-hover>
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
  </v-container>
</template>

<style scoped>
.bio-container {
  position: relative;
}
.edit-icon {
  position: absolute;
  z-index: 999;
  top: 8px;
  right: -15px;
  font-size: 30px;
}
.username {
  padding-top: 20px;
}
.friends {
  text-align: center;
}
#bio-text {
  resize: none !important;
  color: #707070;
}
</style>

<script>
import { getGenericSkynetDownloadLink } from "@/filters/utils";

export default {
  name: "ProfileInfo",
  methods: {
    handleBioUpdate() {
      alert("Update bio here")
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
};
</script>
