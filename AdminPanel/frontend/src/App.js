import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom'

import NavBar from './components/NavBar'
import Landing from './components/Landing'
import Login from './components/Login'
import Register from './components/Register'
import Dashboard from './Dashboard'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Categories from './Categories';

class App extends Component {
  render() {
    return (
      <Router>
        <div className="App">
          <NavBar />
          <Route exact path="/" component={Landing} />
          <div className="container">
            <Route exact path="/register" component={Register} />
            <Route exact path="/login" component={Login} />
            <Route exact path="/dashboard" component={Dashboard} />
            <Route exact path="/categories" component={Categories} />

          </div>
        </div>
      </Router>
    );
  }
}

export default App;
