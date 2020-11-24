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
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="sessionName"
                  label="Session Name"
                  :error-messages="inputError"
                  @input="onInput"
                  :loading="loading"
                  maxlength="100"
                  counter
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <span class="text-body-1 black--text">Private</span>
                <v-switch
                  v-model="isPrivate"
                  :label="isPrivate ? 'Private' : 'Public'"
                ></v-switch>
              </v-col>
              <v-col cols="6">
                <span class="text-body-1 black--text">Session mode</span>
                <v-switch
                  v-model="isLooping"
                  :label="
                    `${isLooping ? 'Cooperative Loop' : 'Music Playlist'}`
                  "
                ></v-switch>
              </v-col>
            </v-row>
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
            @click="create()"
            :loading="loading"
            :disabled="!!inputError"
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
      inputTimeout: null,
      isPrivate: false,
      isLooping: false
    };
  },

  methods: {
    onInput() {
      if (this.inputTimeout) clearTimeout(this.inputTimeout);
      this.inputTimeout = setTimeout(() => {
        this.inputError = "";
        this.loading = true;
        this.fetchSession(this.sessionName)
          .then(data => {
            this.loading = false;
            console.log(data);
            this.inputError = "A session with that name already exists.";
          })
          .catch(error => {
            this.loading = false;
            console.log(error);
          });
      }, 500);
    },

    create() {
      this.loading = false;
      this.createSession(this.sessionName, this.isPrivate, this.isLooping)
        .then(() => {
          console.log(`session ${this.sessionName} created`);
          this.loading = false;
          this.$router.push(`/session/${this.sessionName}`);
        })
        .catch(error => {
          this.loading = false;
          console.error(error);
        });
    }
  }
};
</script>
