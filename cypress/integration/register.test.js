const randomstring = require('randomstring');

const username = randomstring.generate()
const email = `${username}@test.com`;
describe('Register', () => {
    it('should display the registration form', () => {
        cy
            .visit('/register')
            .get('h1').contains('Register')
            .get('form')
    });
    // it('should allow a user to register', () => {
    //     // register user
    //     cy
    //         .visit('/register')
    //         .get('input[name="username"]').type(username)
    //         .get('input[name="email"]').type(email)
    //         .get('input[name="password"]').type('test')
    //         .get('input[type="submit"]').click()
        
    //     cy.contains('All Users')
    //     cy.contains(username)
    //     cy.get('.navbar-burger').click()
    //     cy.get('.navbar-menu').with(() => {
    //         cy
    //             .get('.navbar-item').contains('User Status')
    //             .get('.navbar-item').contains('Log out')
    //             .get('.navbar-item').contains('Log In').should('not.be.visible')
    //     });
    // });
    
});