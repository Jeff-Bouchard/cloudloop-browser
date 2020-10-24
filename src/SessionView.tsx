import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import request from "./utils/request";

import { LoopData } from "./types";

import Grid from "@material-ui/core/Grid";
import { Loop } from "./components/Loop";
import { Typography } from "@material-ui/core";


import { LoopListContainer, UserListContainer } from "./styled";
import Waveform from "./components/Waveform";

const getSessionData = (sessionName: string): any => {
  const url = `loops?session=${sessionName}`;
  const options = { method: "GET" };
  return request(url, options);
};

function SessionView() {
  const [loops, setLoops] = useState<LoopData[]>([]);
  const { sessionName } = useParams();

  useEffect(() => {
    getSessionData(sessionName)
      .then((res: any) => {
        const {
          data: { results },
        } = res;
        setLoops(results);
        console.log(results);
      })
      .catch(() => alert("Something went wrong while fetching loops..."));
  }, [sessionName]);

  return (
    <Grid container justify="center">
      <Grid item xs={4}>
        <Typography variant="h2">Session:</Typography>
        <Typography variant="h4">{sessionName}</Typography>
      </Grid>
      <LoopListContainer item xs={7}>
        {loops.map((loop) => (
          <Waveform key={loop.id} loopData={loop} />
        ))}
      </LoopListContainer>
    </Grid>
  );
}

export default SessionView;