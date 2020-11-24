import Vue from "vue";
import Vuex from "vuex";
import cloudloop from "../mixins/cloudloop";

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
        cloudloop.methods
          .logInUser(userPass.username, userPass.password)
          .then(data => {
            window.localStorage.setItem("JWT", data.data.results);
            dispatch("fetchUser");
            resolve();
          })
          .catch(reject);
      });
    },

    logOutUser({ commit }) {
      return new Promise((resolve, reject) => {
        cloudloop.methods
          .logOutUser()
          .then(() => {
            window.localStorage.removeItem("JWT");
            commit("setLoggedInUser", null);
            resolve();
          })
          .catch(reject);
      });
    }
  },
  modules: {}
});
