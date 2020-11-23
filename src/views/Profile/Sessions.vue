<template>
  <v-row>
    <v-col cols="12" lg="4">
      <v-card @click="newLoopSession" class="session-card add-session-card">
        <v-container fill-height fluid>
          <v-row align="center" justify="center">
            <v-icon class="plus-icon" large>mdi-plus</v-icon>
            <v-card-title class="add-session-title">
              NEW LOOP SESSION
            </v-card-title>
          </v-row>
        </v-container>
      </v-card>
    </v-col>
    <v-col v-if="loading" cols="12" lg="4" align-self="center">
      <v-row justify="center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="90"
        ></v-progress-circular>
      </v-row>
    </v-col>
    <v-col v-for="session in sessions" :key="session.name" cols="12" lg="4">
      <SessionCard :session="session" />
    </v-col>
  </v-row>
</template>

<style scoped>
.add-session-title {
  font-size: 24px;
  text-align: center;
  padding-top: 0;
  width: 70%;
}
.session-card {
  height: 239px;
}
.plus-icon {
  font-size: 100px !important;
  color: gray;
  opacity: 0.5;
}
.add-session-card {
  box-shadow: none !important;
  background-image: url("data:image/svg+xml,%3csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25' fill='none' rx='15' ry='15' stroke='%23333' stroke-width='3' stroke-dasharray='6%2c 14' stroke-dashoffset='0' stroke-linecap='square'/%3e%3c/svg%3e");
  border-radius: 15px;
  opacity: 0.7;
}
</style>

<script>
import SessionCard from "./SessionCard.vue";

export default {
  name: "Sessions",
  components: { SessionCard },
  data() {
    return {
      sessions: [],
      loading: false,
    };
  },
  beforeMount: function () {
    this.fetchUserSessions();
  },
  computed: {
    isOnOwnProfile() {
      const { loggedInUser } = this.$store.state;
      const { userName } = this.$route.params;
      return loggedInUser ? loggedInUser.username === userName : false;
    },
  },
  methods: {
    newLoopSession() {
      alert("Go to new session page");
    },
    fetchUserSessions() {
      this.loading = true;
      const { userName } = this.$route.params;
      const fetchOptions = {
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Authorization: `JWT ${window.localStorage.getItem("JWT")}`,
        },
      };

      fetch(
        `https://dev.cloudloop.io/sessions?username=${userName}`,
        fetchOptions
      )
        .then((response) => {
          if (response.ok) return response.json();
          else console.error(response.status);
        })
        .then(({ data: { results } }) => {
          this.sessions = results;
          this.loading = false;
          console.log("sessions", results);
        });
    },
  },
};
</script>
