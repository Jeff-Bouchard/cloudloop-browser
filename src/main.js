import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import {
  getGenericSkynetDownloadLink,
  getWavDownloadFromProxy,
  getColorForString
} from "./filters/utils.js";
import "@mdi/font/css/materialdesignicons.css";
import VueWaveSurfer from "vue-wave-surfer";
import VueSocketIOExt from "vue-socket.io-extended";
import io from "socket.io-client";
import SearchResults from "@/components/SearchResults.vue";
import WaveformPlayer from "@/components/WaveformPlayer.vue";

const socket = io("https://dev.cloudloop.io");

Vue.config.productionTip = false;
Vue.use(VueWaveSurfer);
Vue.use(VueSocketIOExt, socket);

new Vue({
  sockets: {
    connect() {
      console.log("Socket connect!");
    }
  },
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");

Vue.component("SearchResults", SearchResults);
Vue.component("WaveformPlayer", WaveformPlayer);

Vue.filter("getGenericSkynetDownloadLink", getGenericSkynetDownloadLink);
Vue.filter("getWavDownloadFromProxy", getWavDownloadFromProxy);
Vue.filter("getColorForString", getColorForString);
