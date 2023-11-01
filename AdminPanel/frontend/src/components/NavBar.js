import React, { Component } from 'react';
import {withRouter } from 'react-router-dom'

class NavBar extends Component {
    logOut(e) {
        e.preventDefault()
        localStorage.removeItem('usertoken')
        this.props.history.push('/')
    }

    render() {
        const loginRegLink = (
            <div class="nav-links">

            <a href="/login" >Login</a>
            <a href="/register">Register</a>
            </div>


        )

        const userLink = (
                        <div class="nav-links">

                        <a href="/dashboard" >Dashboard</a>
                        <a href="/categories" >Categories</a>
                        <a href="" onClick={this.logOut.bind(this)} target="_blank">Logout</a>

                        </div>
        )

        return (

<div class="nav">
  <div class="nav-header">
    <div class="nav-title">
    VANGUARD-CENTER

    </div>
  </div>
  <div class="nav-btn">
    <label for="nav-check">
      <span></span>
      <span></span>
      <span></span>
    </label>
  </div>
  
  {localStorage.usertoken ? userLink : loginRegLink}

</div>

        )
    }
}

export default withRouter(NavBar)
