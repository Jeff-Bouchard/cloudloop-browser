<template>
  <v-container>
    <link rel="stylesheet" href="bootstrap.min.css" />
    <link rel="stylesheet" href="style.css" />
    <meta charset="utf-8" />

    <div
      @click="this.destroySession"
      class="show-if-initialized show-if-logged-in logout-bar"
      style="display:none"
    >
      <a href="javascript: skyid.sessionDestroy()">Logout</a>
    </div>

    <div class="hide-if-initialized">
      <h2 class="big-margin">Loading...</h2>
    </div>

    <div class="show-if-initialized hide-if-logged-in" style="display:none">
      <h2>
        Export a standalone library of audio from this session using
        <a href="https://sky-id.hns.siasky.net">SkyID</a> for authentication
      </h2>

      <!-- Button for login -->
      <v-btn @click="sessionStart" class="skyid-button button-blow big-margin">
        <img src="SkyID_Logo_128_white.png" alt="SkyID" class="skyid-logo" />
        Sign in with SkyID
      </v-btn>
    </div>

    <div
      class="show-if-initialized show-if-logged-in small-margin"
      style="display:none"
    >
      <textarea id="note" class="p-3 rounded"> Loading... </textarea><br />
      <div>
        <v-btn
          id="export session"
          class="skyid-button small-margin-top"
          @click="saveSession"
        >
          Export Session
        </v-btn>
      </div>
      <div>
        <v-btn
          id="import_session"
          class="skyid-button small-margin-top"
          @click="fetchSession"
        >
          Import Session
        </v-btn>
      </div>
    </div>

    <footer>
      Read more on
      <a
        href="https://github.com/DaWe35/SkyID-example-note-dapp"
        target="_blank"
        >GitHub</a
      >
      - forked from
      <a
        href="https://skyportal.xyz/_BF4CHsFIichxjdgAFhU-tEKqsoPDxC9OMsWbMkyMbz4KQ/"
        target="_blank"
        >Note to myself</a
      >
    </footer>
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
      this.skyid.getFile(`cloudloop-session`, function(response, revision) {
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
      this.skyid.setFile("cloudloop-session", json, function(response) {
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
      this.skyid.sessionStart();
    }
  }
};
</script>
