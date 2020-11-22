/* eslint-disable no-unused-vars */
import * as mm from "music-metadata";
import { v4 as uuidv4 } from "uuid";
import bytes from "bytes";

export default {
  methods: {
    processFiles(files) {
      return new Promise((resolve, reject) => {
        files.forEach(file => {
          // test for file type
          if (!/^audio\/wav$/.test(file.type))
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
        });
      });
    }
  }
};
