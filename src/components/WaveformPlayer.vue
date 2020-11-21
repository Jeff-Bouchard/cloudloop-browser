<template>
  <v-container fluid>
     <v-row justify="center">
      <v-col align-self="center" cols="12" lg="2">
        <div style="text-align: end">
          <v-btn
            fab
            dark
            large
            x-large
            style="margin: 0"
            class="mr-4"
            color="black"
            @click="playPause"
          >
            <v-icon dark>
              {{ isPlaying ? "pause" : "play_arrow" }}
            </v-icon>
          </v-btn>
        </div>
      </v-col>
      <v-col cols="12" lg="10">
        <div :id="'waveform-' + loop.hash"></div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import WaveSurfer from "wavesurfer.js";
  import {getDownloadLink} from "@/filters/utils";

  export default {
    name: "WaveformPlayer",
    props: ["loop"],
    data() {
      return {
        isPlaying: false
      }
    },
    mounted() {
      const { loop } = this.$props;

      this.waveSurfer = WaveSurfer.create({
        container: `#waveform-${loop.hash}`,
        barWidth: 2,
        barHeight: 8,
        barMinHeight: 1,
        cursorWidth: 1,
        backend: "WebAudio",
        height: 80,
        progressColor: "#3b2898",
        responsive: true,
        waveColor: "#7cecdc",
        cursorColor: "transparent",
      })

      const downloadLink = getDownloadLink(loop.link);
      this.waveSurfer.load(downloadLink);

      // Loop tracks
      this.waveSurfer.on('finish', () => {
        this.waveSurfer.play();
      })
    },

    methods: {
      playPause() {
        this.waveSurfer.playPause();
        this.isPlaying = !this.isPlaying;
      },
      pause() {
        this.waveSurfer.pause();
        this.isPlaying = false;
      },
      play() {
        this.waveSurfer.play();
        this.isPlaying = true;
      },
      playFromStart() {
        this.waveSurfer.play(0);
      }
    }

  };
</script>
