<template>
  <v-card class="user-card">
    <v-row justify="space-around">
      <v-col cols="12" lg="1">
        <v-avatar size="60">
          <img :src="follower.picture_link | getLink" />
        </v-avatar>
      </v-col>
      <v-col cols="12" lg="4" align-self="center">
        <span class="follower-name">{{ follower.username }}</span>
        <span class="follower-count"
          >{{ follower.friend_count }}
          {{ follower.friend_count | pluralize }}</span
        >
      </v-col>
      <v-col cols="12" lg="3" align-self="center">
        <v-btn small dark class="unfollow-btn">
          <v-icon class="unfollow-icon">mdi-heart-outline</v-icon>UNFOLLOW
        </v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>

<style scoped>
.user-card {
  box-shadow: none !important;
  border: 1px solid gray;
  border-radius: 15px;
}
.follower-name {
  font-size: 14px;
  font-weight: 600;
  display: block;
  margin-bottom: -5px;
}
.follower-count {
  font-size: 12px;
}
.unfollow-btn {
  border-radius: 8px;
  margin-left: -20px;
}
.unfollow-icon {
  font-size: 15px;
  margin-left: -5px;
  margin-right: 4px;
  margin-top: -2px;
}
</style>

<script>
import { getDownloadLink } from "@/filters/utils";
export default {
  name: "FollowerCard",
  props: ["follower"],
  filters: {
    getLink(pictureLink) {
      return getDownloadLink(pictureLink);
    },
    pluralize(count) {
      return count > 1 ? "Followers" : "Follower";
    },
  },
  methods: {
    goToFollowerProfile() {
      this.$router.push(`/users/${this.$props.follower.username}`);
    },
  },
};
</script>
