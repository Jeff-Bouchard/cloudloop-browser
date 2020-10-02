import React, { FunctionComponent } from "react";
import Play from "./Play";
import { Grid } from "@material-ui/core";

interface Props {
  play: () => void;
  pause: () => void;
}

const PlayPauseButton: FunctionComponent<Props> = ({ play, pause }) => {
  return (
    <Grid container justify="center" alignItems="center">
      <Grid style={{ marginLeft: 15 }} xs={5} item>
        <Play handleClick={play} />
      </Grid>
    </Grid>
  );
};

export default PlayPauseButton;
