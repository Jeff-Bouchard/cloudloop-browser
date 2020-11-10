<template>
  <v-container class="my-10 px-6">
    <v-row>
      <v-col cols="12">
        <span class="text-h3 text-uppercase font-weight-bold">
          Your Sessions
          <v-tooltip bottom close-delay="500">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                icon
                color="black"
                v-on="on"
                v-bind="attrs"
                @click="isPrivate = !isPrivate"
              >
                <v-icon>{{ isPrivate ? "lock" : "lock_open" }}</v-icon>
              </v-btn>
            </template>
            <span>{{ isPrivate ? "Private" : "Public" }}</span>
          </v-tooltip>
        </span>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6" lg="4" xl="2">
        <v-responsive aspect-ratio="1">
          <Dropzone class="dropzone" @drop="onFile" />
        </v-responsive>
      </v-col>
      <v-col
        cols="12"
        sm="6"
        lg="4"
        xl="2"
        v-for="session in sessions"
        :key="session.id"
      >
        <router-link to="session">
          <v-card>
            <v-responsive aspect-ratio="1">
              <v-img :src="session.coverUrl" />
            </v-responsive>
          </v-card>
        </router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.dropzone {
  width: 100%;
  height: 100%;
}
</style>

<script>
import Dropzone from "@/components/Dropzone.vue";

export default {
  name: "Sessions",

  components: {
    Dropzone
  },

  data() {
    return {
      isPrivate: true,
      sessions: [
        {
          id: 0,
          stars: 100,
          coverUrl:
            "https://skyportal.xyz/HAClCALSAo5HaaELUam8iSp6fAHMik5Oy6sXtAUNIUE8_Q"
        }
      ]
    };
  },

  methods: {
    onFile(event) {
      console.log(event);
      if (event.dataTransfer && event.dataTransfer.files)
        console.log(event.dataTransfer.files);
      this.$router.push("session");
    }
  }
};
</script>
