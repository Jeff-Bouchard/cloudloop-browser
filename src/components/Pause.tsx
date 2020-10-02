import React, { FunctionComponent } from "react";

interface Props {
  onPlayerClick: () => void;
}

const Pause: FunctionComponent<Props> = ({ onPlayerClick }) => {
  return (
    <svg className="button" viewBox="0 0 60 60" onClick={onPlayerClick}>
      <polygon points="0,0 15,0 15,60 0,60" />
      <polygon points="25,0 40,0 40,60 25,60" />
    </svg>
  );
};

export default Pause;
