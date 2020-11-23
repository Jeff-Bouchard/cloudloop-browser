<template>
  <v-row justify="center">
    <v-dialog
      :value="dialog"
      max-width="600px"
      @input="$emit('update:dialog', $event)"
    >
      <v-card>
        <v-card-title>
          <span class="headline">Crate a new session</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-text-field
              v-model="sessionName"
              label="Session Name"
              :error-messages="inputError"
              @input="onInput"
              :loading="loading"
            ></v-text-field>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="$emit('update:dialog', false)">
            Cancel
          </v-btn>
          <v-btn
            color="blue"
            text
            @click="$emit('update:dialog', false)"
            :loading="loading"
          >
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import cloudloop from "@/mixins/cloudloop";

export default {
  name: "NewSessionModal",
  mixins: [cloudloop],
  props: ["dialog"],
  data() {
    return {
      loading: false,
      inputError: "",
      sessionName: "",
      inputTimeout: null
    };
  },

  methods: {
    onInput() {
      if (this.inputTimeout) clearTimeout(this.inputTimeout);
      this.inputTimeout = setTimeout(() => {
        this.loading = true;
        this.fetchSession(this.sessionName)
          .then(data => {
            this.loading = false;
            console.log(data);
            this.inputError = "Session already exists.";
          })
          .catch(error => {
            this.loading = false;
            console.log(error);
          });
      }, 500);
    }
  }
};
</script>
