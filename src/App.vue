<template>
  <v-app>
    <v-app-bar app color="teal" dark>
      <router-link to="/" class="text-decoration-none white--text">
        <v-img
          contain
          width="50"
          alt="cloudloop Logo"
          :src="require('./assets/infinity.svg')"
        />
      </router-link>
      <v-spacer></v-spacer>
      <v-text-field
        dense
        filled
        outlined
        single-line
        v-model="search"
        hide-details="true"
        placeholder="Search cloudloop"
        append-icon="search"
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-btn v-if="!loggedInUser" outlined @click="goToLoginPage">
        Login
      </v-btn>
      <h6
        v-if="!!loggedInUser && !$vuetify.breakpoint.mobile"
        class="text-h6 text-uppercase mr-4"
      >
        {{ loggedInUser.username }}
      </h6>
      <v-menu v-if="!!loggedInUser" offset-y>
        <template v-slot:activator="{ on }">
          <v-avatar color="red" size="40" v-on="on"></v-avatar>
        </template>
        <v-list>
          <router-link
            :to="'/users/' + loggedInUser.username"
            class="text-decoration-none black--text"
          >
            <v-list-item>
              <v-list-item-icon>
                <v-icon>account_circle</v-icon>
              </v-list-item-icon>
              <v-list-item-title>
                My Profile
              </v-list-item-title>
            </v-list-item>
          </router-link>
          <v-list-item @click="logOutUser">
            <v-list-item-icon>
              <v-icon>exit_to_app</v-icon>
            </v-list-item-icon>
            <v-list-item-title v-for="(link, index) in menuLinks" :key="index">
              Logout
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data: () => ({
    search: "",
    menuLinks: [{ text: "My Sessions", to: "sessions" }]
  }),

  mounted() {
    this.$store.dispatch("fetchUser");
  },

  computed: {
    loggedInUser() {
      return this.$store.state.loggedInUser;
    }
  },

  methods: {
    logOutUser() {
      this.$store.dispatch("logOutUser").then(() => {
        this.$router.push("/");
      });
    },
    goToLoginPage() {
      this.$router.push("/login");
    }
  }
};
</script>
