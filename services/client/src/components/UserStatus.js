import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

class UserStatus extends Component {
    constructor (props) {
        super(props);
        this.state = {
            email: '',
            username: '',
            id: '',
            admin: '',
            active: ''
        };
    };
    componentDidMount() {
        if (this.props.isAuthenticated) {
            this.getUserStatus();
        }
    }
    getUserStatus(event) {
        const options = {
            url: `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/status`,
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${window.localStorage.authToken}`
            }
        }
        return axios(options) 
        .then((res) => {
            // console.log(res.data.data)
            this.setState({
                email: res.data.data.email,
                username: res.data.data.username,
                id: res.data.data.id,
                active: String(res.data.data.active),
                admin: String(res.data.data.admin)
            });
        })
        .catch((error) => {console.log(error)})
    }
    render() {
        if (!this.props.isAuthenticated) {
            console.log(this.props.isAuthenticated);
            return (
                <p>You must be logged-in to view this. Click<Link to='/login'>here</Link>to log back in.</p>
            )
        }
        return (
            <div>
                <p>test.</p>
                <li><strong>User Id:</strong>{this.state.id}</li>
                <li><strong>User Email:</strong>{this.state.email}</li>
                <li><strong>User Username:</strong>{this.state.username}</li>
                <li><strong>User Admin:</strong>{this.state.active}</li>
                <li><strong>User Admin:</strong>{this.state.admin}</li>

            </div>
        )
    }

}

export default UserStatus;