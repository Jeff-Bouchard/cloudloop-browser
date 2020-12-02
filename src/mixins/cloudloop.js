import { v4 as uuidv4 } from "uuid";

const baseUrl = "https://dev.cloudloop.io";
// const baseUrl =
//   location.hostname === "localhost"
//     ? "https://dev.cloudloop.io"
//     : "https://cloudloop.io";

const fetchOptions = {
  credentials: "include",
  headers: {
    "Content-Type": "application/json",
    Authorization: `JWT ${window.localStorage.getItem("JWT")}`
  }
};

export default {
  methods: {
    fetchUserSessions(userName) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/sessions?username=${userName}`, fetchOptions)
          .then(response => {
            if (response.ok) return response.json();
            else reject(response.status);
          })
          .then(resolve)
          .catch(reject);
      });
    },

    fetchSession(sessionName) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/session?session_name=${sessionName}`, fetchOptions)
          .then(response => {
            if (response.ok) return response.json();
            else reject(response.status);
          })
          .then(resolve)
          .catch(reject);
      });
    },

    fetchPublicSessionHeaders() {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/publicSessionHeaders`, fetchOptions)
          .then(response => {
            if (response.ok) return response.json();
            else reject(response.status);
          })
          .then(resolve)
          .catch(reject);
      });
    },

    createSession(sessionName, isPrivate = false, isLooping = false) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/session`, {
          ...fetchOptions,
          method: "POST",
          body: JSON.stringify({
            session_name: sessionName,
            private_session: isPrivate,
            is_looping: isLooping
          })
        })
          .then(response => {
            if (response.ok) return response.json();
            else reject(response.status);
          })
          .then(resolve)
          .catch(reject);
      });
    },

    deleteSlot(sessionName, slotId) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/delete_slot`, {
          ...fetchOptions,
          method: "POST",
          body: JSON.stringify({
            session_name: sessionName,
            slot_number: slotId
          })
        })
          .then(response => {
            if (response.ok) return response.json();
            else reject(response.status);
          })
          .then(resolve)
          .catch(reject);
      });
    },

    logInUser(username, password) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/auth/login`, {
          headers: {
            "Content-Type": "application/json"
          },
          method: "POST",
          body: JSON.stringify({
            username,
            password
          })
        })
          .then(response => {
            if (response.ok) return response.json();
            else reject(response.status);
          })
          .then(resolve)
          .catch(reject);
      });
    },

    logOutUser() {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/auth/logout`, { ...fetchOptions, method: "POST" })
          .then(response => {
            if (response.ok) return resolve();
            else reject("Error logging out user");
          })
          .catch(reject);
      });
    },
    joinSession(username, session_name) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/join`, { 
          method: "POST",
          body: JSON.stringify({
            username: username,
            session_name: session_name
          })
         })
        .then(response => {
          if (response.ok) return resolve();
          else reject("Error joining session.")
        })
        .catch(reject);
      });
    },
    uploadAudio(file, username, sessionName) {
      return new Promise((resolve, reject) => {
        fetch(`${baseUrl}/upload`, {
          method: "POST",
          headers: {
            ...fetchOptions.headers,
            "CloudLoop-Loop-Creator": username,
            "CloudLoop-Loop-Session": sessionName,
            "CloudLoop-Loop-Hash": uuidv4()
          },
          body: file
        })
          .then(response => {
            if (response.ok) return resolve();
            else reject("Error logging out user");
          })
          .catch(reject);
      });
    }
  }
};
