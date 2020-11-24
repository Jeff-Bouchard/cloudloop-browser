<template>
  <v-card class="mx-auto" min-width="800" tile>
    <v-list-item v-for="(item, i) in this.sessions" :key="i"
      >Hello
    </v-list-item>
  </v-card>
</template>

<script>
//import SessionCard from "@/components/SessionCard.vue";
//import FollowerCard from "@/views/Profile/FollowerCard.vue";

export default {
  //components: { SessionCard, FollowerCard },
  name: "SearchResults",
  props: ["sessions", "users"]
};
</script>
