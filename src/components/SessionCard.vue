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
          <v-btn
            fab
            icon
            right
            width="40px"
            height="40px"
            class="ml-2 mt-3"
            @click="toggleFavorite"
          >
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
  data() {
    return {
      sessionHeader: {
        created_at: "2020-09-29T21:05:24.379402",
        creator: "datamancer",
        favorited_by: [],
        generation: 0,
        name: "determine it!",
        picture:
          "https://siasky.net/NABSbY8aexCzOBkaC4UuCDpeD0SfJMOeAtIOPdBn93gYZw",
        private: false,
        users: ["datamancer"],
        users_online: {
          datamancer: "2020-09-29T21:05:25.771431"
        }
      }
    };
  }
};
</script>
