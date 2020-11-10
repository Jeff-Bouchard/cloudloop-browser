<template>
  <v-container>
    <v-row>
      <v-col cols="4">
        <v-btn x-large fab dark large color="black">
          <v-icon dark>
            mdi-android
          </v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Session",
  data() {
    return {
      data: require("../../example-data.json")
    };
  }
};
</script>
