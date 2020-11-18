<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/cloudloop-icon.png')"
          class="my-3"
          contain
          height="300"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to cloudloop
        </h1>

        <p class="subheading font-weight-regular">
          Lorem, ipsum dolor sit amet consectetur adipisicing elit. Tenetur<br />
          dicta facere quidem natus vero? Ducimus minima neque, reprehenderit<br />
          quisquam ipsa magni saepe, perspiciatis non earum harum itaque,<br />
          consectetur quod sunt.
        </p>
      </v-col>

      <v-col class="mb-5" cols="12">
        <h2 class="headline font-weight-bold mb-3">
          What's next?
        </h2>

        <v-row justify="center">
          <router-link
            v-for="(next, i) in whatsNext"
            :key="i"
            :to="next.to"
            class="subheading mx-3"
          >
            {{ next.text }}
          </router-link>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Home",
  data: () => ({
    whatsNext: [
      {
        text: "My Sessions",
        to: "sessions"
      }
    ]
  })
};
</script>
