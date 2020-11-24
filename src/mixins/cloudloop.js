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
    }
  }
};
