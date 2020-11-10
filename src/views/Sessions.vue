<template>
  <v-container class="my-10">
    <v-rows>
      <v-col cols="12">
        <span class="text-h3 text-uppercase font-weight-bold">
          Your Sessions
          <v-btn icon color="black" @click="isPrivate = !isPrivate">
            <v-icon>{{ isPrivate ? "lock" : "lock_open" }}</v-icon>
          </v-btn>
        </span>
      </v-col>
    </v-rows>
  </v-container>
</template>

<script>
export default {
  name: "Sessions",
  data() {
    return {
      isPrivate: true
    };
  }
};
</script>
