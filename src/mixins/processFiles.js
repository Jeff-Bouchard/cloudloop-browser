import * as musicMetadata from "music-metadata-browser";
import cloudloop from "@/mixins/cloudloop";
import { v4 as uuidv4 } from "uuid";
import bytes from "bytes";

export default {
  mixins: [cloudloop],
  data() {
  },
  methods: {
    processFiles(files) {
      return new Promise((resolve, reject) => {
        files.forEach(file => {
          // test for file type
          if (!/^(audio\/wav|audio\/x-wav|audio\/wave)$/.test(file.type))
            return reject(`Invalid filetype ${file.type}`);
          // test for file size
          if (file.size > bytes("1 GB"))
            return reject(
              "File too big. Your file(s) should be smaller than 1 GB."
            );
          // add file to store
          this.$store.commit("addFile", {
            file,
            uuid: uuidv4(),
            status: "added",
            fileUrl: URL.createObjectURL(file)
          });
          this.parseFiles();
        });
        resolve();
      });
    },

    parseFiles() {
      // only parse one file at a time
      if (this.$store.state.files.find(file => file.status === "processing"))
        return;

      const file = this.$store.state.files.find(
        file => file.status === "added"
      );

      if (!file) return;

      file.status = "processing";
      this.$store.commit("updateFile", { uuid: file.uuid, newFile: file });

      musicMetadata
        .parseBlob(file.file)
        .then(metadata => {
          file.status = "processed";
          file.metadata = metadata;
          this.$store.commit("updateFile", { uuid: file.uuid, newFile: file });
          // run again untill all added files are parsed
          this.parseFiles();
          this.uploadFiles();
        })
        .catch(error => {
          console.error(error);
          // run again untill all added files are parsed
          this.parseFiles();
        });
    },

    uploadFiles() {
      // only parse one file at a time
      if (this.$store.state.files.find(file => file.status === "uploading"))
        return;

      const file = this.$store.state.files.find(
        file => file.status === "processed"
      );

      if (!file) return;

      const username = this.$store.state.loggedInUser.username;
      const sessionName = this.$store.state.selectedSession.name;

      file.status = "uploading";
      this.$store.commit("updateFile", { uuid: file.uuid, newFile: file });

      this.uploadAudio(file.file, username, sessionName)
        .then(data => {
          console.log("File uploaded");
          console.log(data);
          this.uploadFiles();
          this.loading = false;
        })
        .catch(error => {
          console.error(error);
          this.uploadFiles();
          this.loading=false;
        });
    }
  }
};
