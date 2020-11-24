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
        z-index="10"
        dense
        filled
        outlined
        single-line
        v-model="search"
        hide-details="true"
        placeholder="Search cloudloop"
        append-icon="search"
        :value="search"
        @change="omnisearch"
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
      <v-overlay class="searchresults" :absolute="true" :value="search != ''">
        <div>
          <v-card class="mx-auto" max-width="800" tile>
            <v-list>
              <SessionCard
                class="overflow-y-auto"
                v-for="(session, q) in this.sessionResults"
                :key="q"
                v-bind:sessionHeader="session"
              >
              </SessionCard>
            </v-list>
          </v-card>
        </div>
      </v-overlay>
      <router-view />
    </v-main>
  </v-app>
</template>

<style scoped>
.searchresults {
  max-height: 100vh;
  overflow-y: scroll;
}
</style>

<script>
import SessionCard from "@/components/SessionCard.vue";

export default {
  name: "App",
  components: { SessionCard },
  data: () => ({
    sessionResults: [],
    userResults: [],
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
    omnisearch() {
      console.log("Search");
      const token = window.localStorage.getItem("JWT");
      if (token) {
        const fetchOptions = {
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${token}`
          }
        };
        fetch(
          "https://dev.cloudloop.io/omnisearch?query=" + this.search,
          fetchOptions
        ).then(response => {
          if (response.ok) {
            response.json().then(data => {
              this.userResults = data.data.results.users;
              this.sessionResults = data.data.results.sessions;
              console.log(
                `Got ${this.userResults.length} users and ${this.sessionResults.length} sessions for query ${this.search}`
              );
            });
          } else console.log(response.json().message);
        });
      } else {
        console.log("no jwt");
      }
    },
    goToLoginPage() {
      this.$router.push("/login");
    }
  }
};
</script>
