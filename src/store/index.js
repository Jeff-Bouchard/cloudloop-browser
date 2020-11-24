import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    loggedInUser: null,
    selectedSession: null,
    selectedProfile: null,
    files: []
  },

  getters: {
    filteredFiles: state => status => {
      return state.files.filter(file => file.status === status);
    }
  },

  mutations: {
    setLoggedInUser(state, user) {
      state.loggedInUser = user;
    },

    setSelectedSession(state, value) {
      state.selectedSession = value;
    },

    addFile(state, file) {
      state.files.push(file);
    },

    setSelectedProfile(state, profile) {
      state.selectedProfile = profile;
    },

    updateFile(state, payload) {
      const index = state.files.findIndex(file => file.uuid === payload.uuid);
      state.files[index] = payload.newFile;
    }
  },

  actions: {
    setSelectedSession({ commit }, payload) {
      console.log("Selecting session: " + payload.session.name);
      commit("setSelectedSession", payload.session);
    },
    fetchUserProfile({ commit }, userName) {
      const token = window.localStorage.getItem("JWT");
      if (token) {
        return new Promise((resolve, reject) => {
          const fetchOptions = {
            credentials: "include",
            headers: {
              "Content-Type": "application/json",
              Authorization: `JWT ${token}`
            }
          };
          fetch(
            `https://dev.cloudloop.io/user${
              userName ? `?username=${userName}` : ""
            }`,
            fetchOptions
          )
            .then(response => {
              if (response.ok) return response.json();
              else reject(response.json().message);
            })
            .then(({ data: { results } }) => {
              console.log({ results });
              commit("setSelectedProfile", results);
              resolve(results);
            });
        });
      }
    },
    fetchUser({ commit }) {
      const token = window.localStorage.getItem("JWT");
      if (token) {
        const fetchOptions = {
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            Authorization: `JWT ${token}`
          }
        };
        fetch("https://dev.cloudloop.io/user", fetchOptions)
          .then(response => {
            if (response.ok) return response.json();
            else console.log(response.json().message);
          })
          .then(({ data: { results } }) => {
            commit("setLoggedInUser", results);
          });
      }
    },
    logInUser({ dispatch }, userPass) {
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
            if (response.ok) return response.json();
            else console.log(response.json().message);
          })
          .then(({ data: { results } }) => {
            window.localStorage.setItem("JWT", results);
            dispatch("fetchUser");
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
