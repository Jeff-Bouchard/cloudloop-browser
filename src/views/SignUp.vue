<template>
  <v-container class="fill-height">
    <v-row justify="center">
      <v-col cols="12" md="6" xl="4">
        <v-card class="rounded-lg pa-4">
          <v-card-title class="text-h5 font-weight-medium">
            Create a new account
          </v-card-title>
          <v-card-text>
            <v-form ref="loginForm">
              <v-text-field
                :rules="[rules.required, rules.email]"
                autocomplete="off"
                :loading="loading"
                v-model="email"
                type="email"
                label="E-Mail"
              ></v-text-field>
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
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-btn outlined class="mr-2" to="login">Login</v-btn>
            <v-spacer />
            <v-btn outlined class="mr-2" v-if="!!username">
              Reset Password
            </v-btn>
            <v-btn outlined @click="submitForm" color="success">Sign Up</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "SignUp",
  data() {
    return {
      email: "",
      username: "",
      password: "",
      loading: false,
      rules: {
        required: value => !!value || "Required",
        email: value => /.+@.+\..+/.test(value) || "E-mail must be valid"
      }
    };
  },

  methods: {
    async submitForm() {
      if (!this.$refs.loginForm.validate()) return;

      const fetchOptions = {
        method: "POST"
      };
      this.loading = true;
      try {
        const response = await fetch(
          "https://cloudloop.io/auth/login",
          fetchOptions
        );
        this.loading = false;
        console.log(response.headers);
      } catch (error) {
        console.error(error);
        this.loading = false;
      }
    }
  }
};
</script>
