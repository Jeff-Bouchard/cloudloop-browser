<template>
  <v-container fluid>
    <div class="show-if-logged-in" style="display:none">
      <v-btn
        @click="destroySession"
        class="skyid-button button-blow big-margin"
      >
        Log out of SkyID
      </v-btn>
    </div>
    <div class="show-if-initialized hide-if-logged-in" style="display:none">
      <!-- Button for login -->
      <v-btn @click="sessionStart" class="skyid-button button-blow big-margin">
        Log in with SkyID
      </v-btn>
    </div>
    <v-row>
      <v-col cols="12" lg="8" sm="4" xs="4">
        <v-card color="#707070" dark v-if="this.session" max-width="100vw">
          <div class="d-flex">
            <div>
              <v-card-title
                class="headline"
                v-text="this.session.name"
              ></v-card-title>

              <v-card-subtitle>
                {{ this.session.creator }}
                <br />
                {{
                  new Date(this.session.created_at).toLocaleDateString(
                    undefined,
                    {
                      day: "numeric",
                      month: "short",
                      year: "numeric"
                    }
                  )
                }}
              </v-card-subtitle>
              <v-card-actions>
                <v-btn
                  fab
                  icon
                  right
                  width="40px"
                  height="40px"
                  class="ml-2 mt-3"
                >
                  <v-icon>grade</v-icon>
                  {{ this.session.favorited_by.length }}
                </v-btn>
                <v-btn
                  fab
                  icon
                  right
                  width="40px"
                  height="40px"
                  class="ml-2 mt-3"
                >
                  <v-icon>people_alt</v-icon>
                  {{ session.users.length }}
                </v-btn>

                <v-spacer />
              </v-card-actions>
            </div>
            <v-avatar class="ma-3" width="50%" height="auto" tile>
              <v-img :src="this.session.picture"></v-img>
            </v-avatar>
          </div>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" lg="8">
        <v-card class="mx-auto" tile>
          <v-list shaped style="max-height: 40vh; overflow:scroll;">
            <v-subheader>Loops</v-subheader>
            <v-list-item v-for="(item, i) in this.session.slots" :key="i">
              <v-list-item-icon>
                {{ i }}
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title v-text="item.hash"></v-list-item-title>
                <v-list-item-title v-text="item.creator"></v-list-item-title>
                <v-list-item-title v-text="item.link"></v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>

    <v-col v-if="loading" cols="12" lg="4" align-self="center">
      <v-row justify="center">
        <v-progress-circular
          indeterminate
          color="primary"
          size="90"
        ></v-progress-circular>
      </v-row>
    </v-col>

    <div
      class="show-if-initialized show-if-logged-in small-margin"
      style="display:none"
    >
      <v-row>
        <v-col cols="6">
          <v-btn
            id="export session"
            class="skyid-button small-margin-top"
            @click="saveSession"
          >
            Export Session
          </v-btn>
        </v-col>
        <v-col cols="6">
          <v-btn
            id="import_session"
            class="skyid-button small-margin-top"
            @click="fetchSession"
          >
            Import Session
          </v-btn>
        </v-col>
      </v-row>
    </div>
  </v-container>
</template>

<!-- for testing -->
<!-- <script src="http://idtest.local/skyid.js"></script> -->
<script>
import SkyID from "skyid";

export default {
  name: "Home",
  props: ["session"],
  data: () => ({
    sessionHeaders: [],
    loading: false,
    skyid: null,
    opts: null,
    whatsNext: [
      {
        text: "My Sessions",
        to: "sessions"
      }
    ]
  }),
  beforeMount() {
    var devMode = false;
    if (
      window.location.hostname == "idtest.local" ||
      window.location.hostname == "localhost" ||
      window.location.protocol == "file:"
    ) {
      devMode = true;
    } else {
      devMode = false;
    }
    this.opts = { devMode: devMode };
  },
  mounted() {
    // detect if app is opened on localhost for development
    this.skyid = new SkyID("CloudLoop", this.skyidEventCallback, this.opts);
  },
  methods: {
    skyidEventCallback(message) {
      this.loading = false;
      switch (message) {
        case "login_fail":
          console.log("Login failed");
          break;
        case "login_success":
          console.log("Login succeed!");
          this.fetchSession();
          break;
        case "destroy":
          console.log("Logout succeed!");
          break;
        default:
          console.log(message);
          break;
      }
    },
    fetchSession() {
      // fetch file
      this.skyid.getFile(this.session.name, function(response, revision) {
        console.log(revision);
        if (response == "") {
          // file not found
          console.log("No session exported at this name.");
        } else {
          // success
          var respObs = JSON.parse(response);
          console.log(respObs);
        }
      });
    },
    saveSession() {
      // convert note to json
      var session = this.session;
      console.log(session);
      var json = JSON.stringify({ data: session });

      // upload to registry with SkyID key
      this.skyid.setFile(this.session.name, json, function(response) {
        if (response != true) {
          alert("Sorry, but upload failed :(");
        } else {
          console.log("session exported!");
        }
      });
    },
    destroySession() {
      this.skyid.sessionDestroy();
    },
    sessionStart() {
      this.loading = this.skyid.sessionStart();
    }
  }
};
</script>
