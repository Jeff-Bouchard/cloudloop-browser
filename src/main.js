import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import "roboto-fontface/css/roboto/roboto-fontface.css";
import "material-design-icons-iconfont/dist/material-design-icons.css";
import { getDownloadLink, getColorForString } from "./filters/utils.js";
import '@mdi/font/css/materialdesignicons.css'
import VueWaveSurfer from "vue-wave-surfer";

Vue.config.productionTip = false;
Vue.use(VueWaveSurfer);

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount("#app");

Vue.filter("getDownloadLink", getDownloadLink);
Vue.filter("getColorForString", getColorForString);

