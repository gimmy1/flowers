import React, { Component } from 'react';
import axios from 'axios'
import { Redirect } from 'react-router-dom'

class Form extends Component {
    constructor (props) {
        super(props);
        this.state = {
            formData: {
                username: '',
                email: '',
                password: ''
            }
        }
        this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
    };

    componentDidMount() {
        this.clearForm();
    }
    componentWillReceiveProps(nextProps) {
        /*
        * Called after the initial rendering and before a component receives new props.
        * So if have changes in props, not on the initial rendering, then this method will fire
        * Necessary because we share state for both sign-up/login. This can cause problems with form validation
        * on a route change. /login to /register if state is not cleared out. 
        * If a user validates correctly, and for whatever reason does not submit but navigates to /register, the registration form will
        * automatically be valid. 
        * To prevent this, this lifecycle method fires on a route change and clears the state!
        * Compoare nextProps with props bc React will fire off for strange reasons, and odd times. Compare if you want to do something based 
        * on a prop change!
        */
        if (this.props.formType !== nextProps.formType) {
            this.clearForm();
        }
    }
    clearForm() {
        this.setState({
            formData: {username: '', email: '', password: ''}
        });
    }
    handleFormChange(event) {
        const obj = this.state.formData;
        obj[event.target.name] = event.target.value;
        this.setState(obj);
    }
    handleUserFormSubmit(event) {
        event.preventDefault();
        const formType = this.props.formType;
        const data = {
            email: this.state.formData.email, 
            password: this.state.formData.password
        }
        if (formType === 'register') {
            data.username = this.state.formData.username       
        }
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/{formType.toLowerCase()}`;
        axios.post(url, data)
        .then((res) => {
            this.clearForm();
            this.props.loginUser(res.data.auth_token);
        })
        .catch((err) => { console.log(err); })
    }

    render() {
        if (this.props.isAuthenticated) {
            return <Redirect to='/' />
        }
        return (
            <div>
                <h1 className='title is-1'>{this.props.formType}</h1>
                <hr/><br/>
                <form onSubmit={(event) => this.handleUserFormSubmit(event)}>
                    {this.props.formType === 'Register' &&
                        <div className="field">
                            <input
                                name="username"
                                className="input is-medium"
                                type="text"
                                placeholder="Enter a username"
                                required
                                value={this.state.formData.email}
                                onChange={this.handleFormChange}
                            />
                        </div>
                    }
                    <div className="field">
                        <input
                            name="email"
                            className="input is-medium"
                            type="email"
                            placeholder="Enter an email address"
                            required
                            value={this.state.formData.email}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <div className="field">
                        <input
                            name="password"
                            className="input is-medium"
                            type="password"
                            placeholder="Enter a password"
                            required
                            value={this.state.formData.email}
                            onChange={this.handleFormChange}
                        />
                    </div>
                    <input
                        type="submit"
                        className="button is-primary is-medium is-fullwidth"
                        value="Submit"
                    />
                </form>
            </div>
        )
    }
}

export default Form;