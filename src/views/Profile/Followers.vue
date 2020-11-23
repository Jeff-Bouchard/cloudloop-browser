<template>
  <v-row>
    <v-col
      :key="follower.username"
      v-for="follower in followers"
      cols="12"
      lg="6"
      class="user-container"
    >
      <FollowerCard :follower="follower" />
    </v-col>
  </v-row>
</template>

<style scoped>
.user-container {
  padding: 5px;
}
</style>

<script>
import FollowerCard from "./FollowerCard.vue";

export default {
  name: "Followers",
  props: ["followers"],
  components: { FollowerCard },
};
</script>
