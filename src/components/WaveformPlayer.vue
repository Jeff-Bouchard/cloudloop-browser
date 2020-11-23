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
      <v-col class="waveform-wrapper" cols="12" lg="10" align-self="center">
        <v-icon
          medium
          @click="toggleStar"
          class="icon star-icon"
          :style="isStarred && 'color: gold'"
        >
          {{ isStarred ? "star" : "mdi-star-outline" }}
        </v-icon>
        <v-icon medium @click="downloadLoop" class="icon download-icon">
          mdi-download-circle
        </v-icon>
        <v-progress-linear
          class="percent-loaded"
          v-if="percentLoaded < 100"
          :value="percentLoaded"
          color="#3b2898"
          background-color="#7cecdc"
          height="2"
        ></v-progress-linear>
        <div :id="'waveform-' + loop.hash"></div>
        <p class="wave-tag creator-tag">
          <span>
            <strong>CREATOR: </strong>
          </span>
          <span class="tag-value">{{ loop.creator }}</span>
        </p>
        <p class="wave-tag created-on-tag">
          <span>
            <strong>CREATED ON: </strong>
          </span>
          <span class="tag-value">{{ loop.created_at | formatDate }}</span>
        </p>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.percent-loaded {
  position: absolute;
  top: 50px;
}
.waveform-wrapper {
  position: relative;
}
.wave-tag {
  position: absolute;
  font-size: 12px;
}
.creator-tag {
  right: 45%;
}
.created-on-tag {
  right: 12%;
}
.tag-value {
  font-size: 12px;
  color: #646464;
}
.icon {
  position: absolute;
  z-index: 3;
}
.star-icon {
  right: 6%;
}
.download-icon {
  right: 0;
  color: black;
}
</style>

<script>
import WaveSurfer from "wavesurfer.js";
import { getWavDownloadFromProxy } from "@/filters/utils";

export default {
  name: "WaveformPlayer",
  props: ["loop"],
  data() {
    return {
      isPlaying: false,
      isStarred: false,
      percentLoaded: 0
    };
  },
  mounted() {
    const { loop } = this.$props;

    this.waveSurfer = WaveSurfer.create({
      container: `#waveform-${loop.hash}`,
      barWidth: 2,
      barHeight: 3,
      barMinHeight: 1,
      cursorWidth: 1,
      backend: "WebAudio",
      height: 80,
      progressColor: "#079688",
      responsive: true,
      waveColor: "#76CCC4",
      cursorColor: "transparent"
    });

    const downloadLink = getWavDownloadFromProxy(loop.link);
    this.waveSurfer.load(downloadLink);

    // Loop tracks
    this.waveSurfer.on("finish", () => {
      this.waveSurfer.play();
    });
    this.waveSurfer.on("loading", percent => {
      this.percentLoaded = percent;
    });
  },

  methods: {
    downloadLoop() {
      const downloadLink = getWavDownloadFromProxy(this.$props.loop.link);
      location.href = downloadLink;
    },
    toggleStar() {
      this.isStarred = !this.isStarred;
    },
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
  },
  filters: {
    formatDate(dateStr) {
      const dateObj = new Date(dateStr);
      return (
        dateObj.getFullYear() +
        "-" +
        (dateObj.getMonth() + 1) +
        "-" +
        dateObj.getDate()
      );
    }
  }
};
</script>
