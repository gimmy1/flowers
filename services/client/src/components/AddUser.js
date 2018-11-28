import React from 'react';

const AddUser = (props) => { // functional component
    return (
        <form onSubmit={(event) => props.addUser(event)}>
            <div className='field'>
                <input
                    name='username'
                    className='input is-large'
                    type='text'
                    placeholder='Enter a username'
                    required
                    value={props.username} // defines the values of input from Parent component
                    onChange={props.handleChange}
                />
            </div>
            <div>
                <input
                    name='email'
                    className='input is-large'
                    type='text'
                    placeholder='Enter an email'
                    required
                    value={props.email} // defines the values of input from Parent component
                    onChange={props.handleChange}
                />
            </div>
            <div>
                <input
                    type='submit'
                    className='button is-primary is-large is-fullwidth'
                    value='Submit'
                />
            </div>
        </form>
    )
}

export default AddUser;
