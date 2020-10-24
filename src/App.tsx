import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";

import SessionView from "./SessionView";

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/">
          <h1>Home</h1>
        </Route>
        <Route path="/browser/session/:sessionName">
          <SessionView />
        </Route>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
