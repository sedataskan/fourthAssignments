import React from "react";
import Login from "./login";

const Console = () => {
  return (
    <div className="console">
      <div className="columns">
        <div className="column1">
          <p className="labels">Local</p>
          <body className="local" />
        </div>
        <div className="column2">
          <p className="labels">Remote</p>
          <body className="remote" />
        </div>
      </div>
      <Login />
    </div>
  );
};

export default Console;
