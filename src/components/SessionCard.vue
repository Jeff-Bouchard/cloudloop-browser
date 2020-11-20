<template>
  <v-card color="pink" dark v-if="sessionHeader" max-width="600">
    <div class="d-flex flex-no-wrap justify-space-between">
      <div>
        <v-card-title
          class="headline"
          v-text="sessionHeader.name"
        ></v-card-title>

        <v-card-subtitle>
          {{ sessionHeader.creator }}
          <br />
          {{
            new Date(sessionHeader.created_at).toLocaleDateString(undefined, {
              day: "numeric",
              month: "short",
              year: "numeric"
            })
          }}
        </v-card-subtitle>
        <v-card-actions>
          <v-btn fab icon right width="40px" height="40px" class="ml-2 mt-3">
            <v-icon>grade</v-icon>
            {{ sessionHeader.favorited_by.length }}
          </v-btn>
          <v-spacer />
        </v-card-actions>
      </div>
      <v-avatar class="ma-3" size="125" tile>
        <v-img :src="sessionHeader.picture"></v-img>
      </v-avatar>
    </div>
  </v-card>
</template>

<script>
export default {
  name: "SessionCard",
  props: ["sessionHeader"]
};
</script>
