import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false
  },
  mutations: {
    setIsLoggedIn(state, value) {
      state.isLoggedIn = value;
    }
  },
  actions: {
    logInUser({ commit }) {
      setTimeout(() => {
        commit("setIsLoggedIn", true);
      }, 500);
    },
    logOutUser({ commit }) {
      setTimeout(() => {
        commit("setIsLoggedIn", false);
      }, 500);
    }
  },
  modules: {}
});
