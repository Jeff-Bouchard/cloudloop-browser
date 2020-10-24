import React, { FunctionComponent, useEffect, useRef } from "react";
import WaveSurfer from "wavesurfer.js";

import { Grid, Typography } from "@material-ui/core";
import PlayPauseBtn from "../PlayPauseBtn";
import { LoopContainer, BtnContainer } from "./styled";

import { LoopData } from "../../types";

interface Props {
  loopData: LoopData;
}

export const Loop: FunctionComponent<Props> = ({
  loopData: {
    id,
    fields: { Download },
  },
}) => {
  const waveformRef = useRef();
  useEffect(() => {
    if (waveformRef.current) {
      const wavesurfer = WaveSurfer.create({
        container: waveformRef.current as any,
        waveColor: "violet",
        progressColor: "purple",
      });
      wavesurfer.load(Download);
    }
  }, []);

  const playAudio = (id: string) => () => {
    const audioEl = document.getElementById(id) as HTMLMediaElement;
    audioEl && audioEl.play();
  };

  const pauseAudio = (id: string) => () => {
    const audioEl = document.getElementById(id) as HTMLMediaElement;
    audioEl.pause();
  };

  const downloadAudio = (id: string) => {
    const audioEl = document.getElementById(id) as HTMLMediaElement;
    window.location.assign(audioEl.src);
  };

  return (
    <Grid>
      <LoopContainer>
        <audio id={id} src={Download} loop>
          Your browser does not support the
          <code>audio</code> element.
        </audio>
        <BtnContainer container justify="center" alignItems="center">
          <Grid item>
            <PlayPauseBtn play={playAudio(id)} pause={pauseAudio(id)} />
          </Grid>
        </BtnContainer>
      </LoopContainer>
      <Grid ref={waveformRef as any}></Grid>
    </Grid>
  );
};
