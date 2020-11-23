<template>
  <v-hover open-delay="50" close-delay="50" v-slot="{ hover }">
    <v-card @click="goToSessionDetail" class="session-card">
      <v-img :src="sessionImg" class="align-end white--text">
        <v-card-title v-if="hover">
          {{ session.name }}
        </v-card-title>
        <v-row class="avatar-container">
          <v-col cols="12" lg="9">
            <v-tooltip v-for="user in session.users" :key="user" top>
              <template v-slot:activator="{ on, attrs }">
                <v-avatar
                  class="avatar"
                  :color="user | getColor"
                  size="33"
                  @click="user | goToProfile"
                  v-bind="attrs"
                  v-on="on"
                >
                </v-avatar>
              </template>
              <span>{{ user }}</span>
            </v-tooltip>
          </v-col>
          <v-col cols="12" lg="3" align-self="center">
            <div class="favorites-container">
              <span class="num-favorites">{{ numFavorites }}</span>
              <v-icon class="star-icon"> mdi-star-outline </v-icon>
            </div>
          </v-col>
        </v-row>
      </v-img>
    </v-card>
  </v-hover>
</template>

<style scoped>
.session-card {
  opacity: 0.9;
  transition: 0.2s;
}
.session-card:hover {
  opacity: 1;
}
.avatar-container {
  padding-left: 8px;
  margin-bottom: -5px;
}
.avatar {
  z-index: 999;
}
.avatar:not(:first-child) {
  margin-left: -10px;
}
.avatar:hover {
  z-index: 1000;
}
.favorites-container {
  position: relative;
}
.num-favorites {
  color: white;
  font-weight: 600;
  position: absolute;
  right: 40px;
  bottom: -21px;
}
.star-icon {
  color: white;
  position: absolute;
  right: 4px;
  bottom: -20px;
}
</style>

<script>
import { getDownloadLink, getColorForString } from "@/filters/utils";

export default {
  name: "SessionCard",
  props: ["session"],
  computed: {
    sessionImg() {
      return getDownloadLink(this.$props.session.picture);
    },
    numFavorites() {
      return this.$props.session.favorited_by.length;
    },
  },
  filters: {
    getColor(userName) {
      return getColorForString(userName);
    },
    goToProfile(userName) {
      this.$router.push(`/users/${userName}`);
    },
  },
  methods: {
    goToSessionDetail() {
      this.$router.push(`/session/${this.$props.session.name}`);
    },
  },
};
</script>