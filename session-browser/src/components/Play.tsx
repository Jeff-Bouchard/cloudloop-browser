import React, { FunctionComponent } from "react";

interface Props {
  handleClick: () => void;
}

const Play: FunctionComponent<Props> = ({ handleClick }) => {
  return (
    <svg
      style={{ cursor: "pointer" }}
      className="button"
      viewBox="0 0 60 60"
      onClick={handleClick}
    >
      <polygon points="0,0 50,30 0,60" />
    </svg>
  );
};

export default Play;
