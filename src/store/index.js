import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loggedInUser: null,
    selectedSession: null,
    selectedProfile: null,
  },
  mutations: {
    setLoggedInUser(state, value) {
      state.loggedInUser = value;
    },
    setSelectedSession(state, value) {
      state.selectedSession = value;
    },
    setSelectedProfile(state, value) {
      state.selectedProfile = value;
    }
  },
  actions: {
    setSelectedSession({ commit }, payload) {
      console.log("Selecting session: " + payload.session.name);
      commit("setSelectedSession", payload.session);
    },
    fetchUserProfile({ commit }, userName) {
      return new Promise((resolve, reject) => {
        const fetchOptions = {
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${window.localStorage.getItem("JWT")}`
          }
        };
  
        fetch(
            "https://dev.cloudloop.io/user?username=" + userName,
            fetchOptions
        ).then(response => {
            if (response.ok) return response.json()
            else reject(response.json().message);
          })
          .then(({data: {results}}) => {
            console.log({results})
            commit('setSelectedProfile', results);
            resolve(results);
          })
      });
    },
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
              response.json().then(jsonData => {
                window.localStorage.setItem("JWT", jsonData.data.results);
              });
              commit("setLoggedInUser", userPass.username);
              resolve(userPass.username);
            } else {
              reject(response.json().message);
            }
          })
          .catch(error => {
            reject(error);
          });
      });
    },

    logOutUser({ commit }) {
      return new Promise((resolve, reject) => {
        const fetchOptions = {
          method: "POST",
          credentials: "include"
        };

        fetch("https://dev.cloudloop.io/auth/logout", fetchOptions)
          .then(response => {
            if (response.ok) {
              commit("setLoggedInUser", null);
              window.localStorage.removeItem("JWT");
              resolve();
            } else {
              reject("Error logging out user");
            }
          })
          .catch(error => {
            reject(error);
          });
      });
    }
  },
  modules: {}
});
