import React, { useEffect, useState, FunctionComponent, useRef } from "react";
import WaveSurfer from "wavesurfer.js";

import Grid from "@material-ui/core/Grid";
import PlayArrowRoundedIcon from "@material-ui/icons/PlayArrowRounded";
import PauseRoundedIcon from "@material-ui/icons/PauseRounded";
import { WaveformContianer, Wave, PlayButton, DownloadLink } from "./styled";
import { Typography } from "@material-ui/core";

const DOWNLOAD_HOST = "http://0.0.0.0:56002";

const Waveform: FunctionComponent<any> = (props) => {
  const { loopData } = props;
  const [playing, setPlaying] = useState(false);
  const [waveform, setWaveform] = useState<any>();
  const waveformRef = useRef<any>();

  useEffect(() => {
    if (waveformRef.current) {
      const newWaveform = WaveSurfer.create({
        barWidth: 3,
        cursorWidth: 1,
        container: waveformRef.current,
        backend: "WebAudio",
        height: 80,
        progressColor: "#2D5BFF",
        responsive: true,
        waveColor: "#EFEFEF",
        cursorColor: "transparent",
      });

      // const audioSource = `${DOWNLOAD_HOST}/download?skylink=${loopData.fields.link}`;
      const audioSource =
        "https://www.mfiles.co.uk/mp3-downloads/gs-cd-track2.mp3";
      newWaveform.load(audioSource);
      setWaveform(newWaveform);
    }
  }, []);

  const handleClick = () => {
    setPlaying(!playing);
    if (waveform) waveform.playPause();
  };

  return (
    <WaveformContianer container>
      <Grid container justify="flex-end" alignContent="center" item xs={2}>
        <Grid item>
          <PlayButton onClick={handleClick}>
            {playing ? (
              <PauseRoundedIcon fontSize="large" />
            ) : (
              <PlayArrowRoundedIcon fontSize="large" />
            )}
          </PlayButton>
        </Grid>
      </Grid>
      <Grid container item xs={10} alignContent="center">
        <Wave ref={waveformRef} />
        <Typography
          style={{ margin: "-20 0 0 10", zIndex: 999 }}
          variant="caption"
        >
          By: {loopData.fields.creator} |{" "}
          <DownloadLink href={loopData.fields.Download} download>
            Download
          </DownloadLink>
        </Typography>
      </Grid>
    </WaveformContianer>
  );
};

export default Waveform;
