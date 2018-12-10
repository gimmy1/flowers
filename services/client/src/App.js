import React, { Component } from 'react';
import axios from 'axios'
import { Route, Switch } from 'react-router-dom';

import UsersList from './components/UsersList'
import AddUser from './components/AddUser'
import About from './components/About'

class App extends Component {
    // use of class based component for statfulness
    constructor() {
        super();
        this.state = {
            users: [],
            username:'',
            email:''
        };
        this.addUser = this.addUser.bind(this); // bound the context of this; 
        this.handleChange = this.handleChange.bind(this); // bound the context of this; 
    }

    // lifecycle methods
    componentDidMount() {
        this.getUsers()
    }
    getUsers() {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/flowers`)
        // .then((res) => { console.log(res.data.data) })  
        .then((res) => { this.setState({ users: res.data.data.users }); })
        .catch((err) => {console.log(err) }) 
    }

    addUser(event) {
        event.preventDefault();
        // new
        const data = {
          username: this.state.username,
          email: this.state.email
        };
        // new
        axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}/flowers`, data)
        .then((res) => {
            this.getUsers();
            this.setState({username: '', email: ''})
        })
        // .then((res) => { console.log(res); })
        .catch((err) => { console.log(err); });
      };

    handleChange(event) {
        // update the state in parent component so it updates when user enters text
        const obj = {}
        obj[event.target.name] = event.target.value;
        this.setState(obj);
    }

    render() {
        return (
            <section className="section">
                <div className="container">
                    <div className="columns">
                        <div className="column is-half">
                        <br/>
                            <Switch>
                                <Route exact path='/' render={ () => (
                                    <div>
                                        <h1 className="title is-1 is-1">All Users</h1>
                                        <hr/><br/>
                                        <AddUser
                                            username={this.state.username}
                                            email={this.state.email}
                                            addUser={this.addUser}
                                            handleChange={this.handleChange}
                                        />
                                        <br/><br/>
                                        <UsersList users={this.state.users}/>
                                    </div>
                                )} />
                                <Route exact path='/about' component={About}/>
                            </Switch>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}

export default App;
