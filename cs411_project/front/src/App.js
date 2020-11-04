import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import {BrowserRouter as Router, Link, Route, Switch} from "react-router-dom";

import Login from './components/Login'

class App extends Component {
  render () {
    return (
      <Router>
        <div className="App">
          <div>
            <Link to = '/'>Home</Link> <Link to ='/login'>Login</Link>
          </div>
          <Switch>
            <Route component = {Login} path = "/login"/>
          </Switch>
        </div>
      </Router>

    );
  }
 
};

export default App;
