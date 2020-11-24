<template>
  <v-container class="fill-height">
    <v-row justify="center">
      <v-col cols="12" md="6" xl="4">
        <v-card class="rounded-lg pa-4">
          <v-card-title class="text-h5 font-weight-medium">
            Login
          </v-card-title>
          <v-card-text>
            <v-form ref="loginForm" @submit="submitForm">
              <v-text-field
                :rules="[rules.required]"
                autocomplete="off"
                v-model="username"
                :loading="loading"
                label="Username"
              ></v-text-field>
              <v-text-field
                :rules="[rules.required]"
                :loading="loading"
                v-model="password"
                label="Password"
                type="password"
                :error-messages="loginError"
              ></v-text-field>
              <input type="submit" class="d-none" />
            </v-form>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-btn outlined class="mr-2" to="sign-up">Sign Up</v-btn>
            <v-spacer />
            <v-btn
              outlined
              class="mr-2"
              v-if="!!username"
              @click="resetPassword()"
            >
              Reset Password
            </v-btn>
            <v-btn outlined @click="submitForm" :loading="loading">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      loginError: "",
      loading: false,
      rules: {
        required: value => !!value || "Required"
      }
    };
  },

  methods: {
    async submitForm(event) {
      if (event) event.preventDefault();
      if (!this.$refs.loginForm.validate()) return;
      this.loading = true;
      this.loginError = "";
      this.$store
        .dispatch("logInUser", {
          username: this.username,
          password: this.password
        })
        .then(() => {
          this.loading = false;
          this.$router.push("/");
        })
        .catch(error => {
          this.loading = false;
          this.loginError = "Error logging in";
          console.log("error logging in");
          console.error(error);
        });
    },

    resetPassword() {
      void 0;
    }
  }
};
</script>
