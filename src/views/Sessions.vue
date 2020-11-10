<template>
  <v-container class="my-10">
    <v-row>
      <v-col cols="12">
        <span class="text-h3 text-uppercase font-weight-bold">
          Your Sessions
          <v-btn icon color="black" @click="isPrivate = !isPrivate">
            <v-icon>{{ isPrivate ? "lock" : "lock_open" }}</v-icon>
          </v-btn>
        </span>
      </v-col>
      <v-col cols="4">
        <Dropzone style="height: 300px; width: 300px;" @drop="onFile" />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Dropzone from "@/components/Dropzone.vue";

export default {
  name: "Sessions",

  components: {
    Dropzone
  },

  data() {
    return {
      isPrivate: true
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
