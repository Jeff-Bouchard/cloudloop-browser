import styled from "styled-components";
import Grid from "@material-ui/core/Grid";

export const WaveformContianer = styled(Grid)`
  margin: 20px;
`;

export const Wave = styled(Grid)`
  width: 100%;
  height: 82px;
`;

export const PlayButton = styled.button`
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80px;
  height: 80px;
  background: #efefef;
  border-radius: 50%;
  border: none;
  outline: none;
  cursor: pointer;
  padding-bottom: 3px;
  &:hover {
    background: #ddd;
  }
`;

export const DownloadLink = styled.a`
  color: black;
  text-decoration: none;
  cursor: pointer;
  &:hover {
    color: blue;
  }
`;
