import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loggedInUser: null
  },
  mutations: {
    setLoggedInUser(state, value) {
      state.loggedInUser = value;
    }
  },
  actions: {
    logInUser({ commit }, userPass) {
      return new Promise((resolve, reject) => {
        const fetchOptions = {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            username: userPass.username,
            password: userPass.password
          })
        };

        fetch("https://dev.cloudloop.io/auth/login", fetchOptions)
          .then(response => {
            if (response.ok) {
              commit("setLoggedInUser", userPass.username);
              resolve(userPass.username);
            } else {
              reject(response.json().message);
            }
          })
          .catch(error => {
            console.error(error);
            reject(error);
          });
      });
    },

    logOutUser({ commit }) {
      setTimeout(() => {
        commit("setIsLoggedIn", false);
      }, 500);
    }
  },
  modules: {}
});
