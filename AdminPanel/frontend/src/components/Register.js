import React, { Component } from 'react'
import { register } from './UserFunctions'

class Register extends Component {

    constructor() {
        super()
        this.state = {
            first_name: '',
            last_name: '',
            email: '',
            password: ''
        }
    }

    onChange = e => {
        this.setState({ [e.target.name]: e.target.value })
    }

    onSubmit = e => {
        e.preventDefault()

        const newUser = {
            first_name: this.state.first_name,
            last_name: this.state.last_name,
            email: this.state.email,
            password: this.state.password
        }

        register(newUser).then(res => {
            this.props.history.push('/login')

        })
    }

    render() {
        return (

                            <div class="login-box">
                            <h2>Register</h2>
                            <form noValidate onSubmit={this.onSubmit}>
                                <div class="user-box">
                                <input type="text"
                                    className="form-control"
                                    name="first_name"
                                    placeholder="Enter First Name"
                                    value={this.state.first_name}
                                    onChange={this.onChange} />
                                <label htmlFor="first_name">First Name</label>
                                 </div>
                            <div class="user-box">
                                <input type="text"
                                    className="form-control"
                                    name="last_name"
                                    placeholder="Enter last Name"
                                    value={this.state.last_name}
                                    onChange={this.onChange} />
                                <label htmlFor="last_name">Last Name</label>
                                </div>
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
                                Register      
                             <span></span>
                            <span></span>
                            <span></span>
                            <span></span>
                            </button>
                    </form>
                    </div>

    
)
}

}
export default Register