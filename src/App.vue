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
      <v-btn v-if="!loggedInUser" outlined to="login">
        Login
      </v-btn>
      <v-menu v-if="!!loggedInUser" offset-y>
        <template v-slot:activator="{ on }" v-if="!$vuetify.breakpoint.mobile">
          <h6 class="text-h6 text-uppercase mr-4" v-on="on">
            {{ loggedInUser }}
          </h6>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title v-for="(link, index) in menuLinks" :key="index">
              <router-link
                :to="link.to"
                class="text-decoration-none black--text"
              >
                {{ link.text }}
              </router-link>
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-menu v-if="!!loggedInUser" offset-y>
        <template v-slot:activator="{ on }">
          <v-avatar color="red" size="40" v-on="on"></v-avatar>
        </template>
        <v-list>
          <v-list-item>
            <v-list-item-title v-for="(link, index) in menuLinks" :key="index">
              <router-link
                :to="link.to"
                class="text-decoration-none black--text"
              >
                {{ link.text }}
              </router-link>
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

  computed: {
    loggedInUser() {
      return this.$store.state.loggedInUser;
    }
  }
};
</script>
