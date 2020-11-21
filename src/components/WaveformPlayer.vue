<template>
  <div class="d-flex flex-no-wrap justify-space-between">
    <vue-wave-surfer
      wavecolor="#EFEFEF"
      :name="wsName"
      :url="this.props.audioURL"
      :options="options"
      :on="on"
    ></vue-wave-surfer>
  </div>
</template>
<script>
export default {
  data() {
    return {
      name: "WaveformPlayer",
      props: ["audioURL"],
      options: {},
      wsName: "tes1t"
    };
  }
};
</script>
