<template>
<v-container>
<v-col v-if="processing" cols="4" lg="4" align-self="center">
        <v-row justify="center">
          <v-progress-circular
            indeterminate
            color="primary"
            size="90"
          ></v-progress-circular>
        </v-row>
      </v-col>
      <v-col cols="12">
      <div
    class="dropzone pa-8"
    :class="`dragover-${isDragOver}`"
    @drop="onDrop"
    @dragover="onDrag"
    @dragenter="onDrag"
    @click="$refs.file.click()"
    @dragend="isDragOver = false"
    @dragleave="isDragOver = false"
    @mouseleave="isDragOver = false"
  >
    <input
      multiple
      ref="file"
      type="file"
      name="files[]"
      accept=".wav"
      @change="onFile"
    />
    <v-img :src="require('../assets/Waves.svg')" contain height="64"></v-img>
    <label class="text-h6 font-weight-black text-center" for="file">
      DROP A .WAV IT LIKE IT'S HOT
    </label>
  </div>
  </v-col>
</v-container>

  
</template>

<style scoped>
.dropzone {
  background-color: white;
  /* Generated using https://kovart.github.io/dashed-border-generator/ */
  background-image: url("data:image/svg+xml,%3csvg width='100%25' height='100%25' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='100%25' height='100%25' fill='none' rx='32' ry='32' stroke='lightgray' stroke-width='3' stroke-dasharray='10' stroke-dashoffset='0' stroke-linecap='square'/%3e%3c/svg%3e");
  border-radius: 32px;
  transition: background 100ms;
  display: grid;
  place-items: center;
}

.dropzone,
.dropzone > * {
  cursor: pointer;
}

input[type="file"] {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}

.dropzone:hover,
.dragover-true {
  background-color: #f9f9f9;
}
</style>

<script>
import processFiles from "../mixins/processFiles";

export default {
  name: "Dropzone",

  mixins: [processFiles],

  data() {
    return {
      loading: false,
      processing: false,
      isDragOver: false
    };
  },

  methods: {
    onDrop(event) {
      this.processing = true;
      event.preventDefault();
      if (event.dataTransfer && event.dataTransfer.files) {
        this.processFiles(event.dataTransfer.files).catch(error => {
          this.processing = false;
          console.error(error);
        });
      }
    },

    onDrag(event) {
      event.preventDefault();
      this.isDragOver = true;
    },

    onFile(event) {
      event.preventDefault();
      this.processing = true;
      if (event.target.files) {
        this.processFiles(event.target.files).then(data => {
          console.log(`File processed:  ${data}`)
          this.processing = false;
        })
        .catch(error => {
          console.error(error);
          this.processing = false;
        });
      }
    }
  }
};
</script>
