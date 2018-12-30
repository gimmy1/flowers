const randomstring = require('randomstring');

const username = randomstring.generate()
const email = `${username}@test.com`

describe('Login', () => {
    it('should display login form', () => {
        cy
            .visit('/login')
            .get('h1').contains('Login')
            .get('form')
    });
    // it('should allow a user to sign in', () => {
    //     // register user
    //     cy
    //         .visit('/register')
    //         .get('input[name="username"]').type(username)
    //         .get('input[name="email"]').type(email)
    //         .get('input[name="password"]').type('test')
    //         .get('input[type="submit"]').click()
        
    //     // log user out
    //     // cy.get('.navbar-burger').click()
    //     // cy.contains('Log Out').click()

    //     // Log user in
    //     cy
    //         .get('a').contains('Log In').click()
    //         .get('input[name="email"]').type(email)
    //         .get('input[name="password"]').type('test')
    //         .get('input[type="submit"]').click()
    //         .wait(100);
        
    //     // assert user is redirected to /
    //     cy.contains('All Users')
    //     cy
    //         .get('table')
    //         .find('tbody > tr').last()
    //         .find('td').contains(username);
        
    //     // log user out
    //     cy
    //         .get('a').contains('Log Out').click();
        
    //     // assert log out is displayed properly
    //     cy.get('p').contains('You are now logged out.')
    //     cy
    //         .get('.navbar-item').contains('User Status').should('not.be.visible')
    //         // .get('.navbar-item').contains('Log In')
    // })
})

