import React, { Component } from 'react'
import { login } from './UserFunctions'

class Login extends Component {

    constructor() {
        super()
        this.state = {
            email: '',
            password: ''
        }
    }

    onChange = e => {
        this.setState({ [e.target.name]: e.target.value })
    }

    onSubmit = e => {
        e.preventDefault()

        const user = {
            email: this.state.email,
            password: this.state.password
        }

        login(user).then(res => {
            if (!res.error) {
                this.props.history.push('/dashboard')
            }
        })
    }

    render() {
        return (
   <div>
                        <div class="login-box">
                            <h2>Login</h2>
                            <form noValidate onSubmit={this.onSubmit}>
                                <div class="user-box">
                                                            <input type="email"
                                                                className="form-control"
                                                                name="email"
                                                                placeholder="Enter Email"
                                                                value={this.state.email}
                                                                onChange={this.onChange} />
                                <label htmlFor="email">Email Address</label>
                                </div>
                             <div class="user-box">
                                <input type="password"
                                    className="form-control"
                                    name="password"
                                    placeholder="Enter Password"
                                    value={this.state.password}
                                    onChange={this.onChange} />      
                                <label htmlFor="password">Password</label>
                                    </div>
                                    <button type="submit" className="btn btn-lg btn-primary btn-block subm">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                         Login
                                    </button>
                                </form>
                                </div>

                                </div>
        )
    }

}
export default Login