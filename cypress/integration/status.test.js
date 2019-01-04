const randomstring = require('randomstring');

const username = randomstring.generate()
const email = `${username}@test.com`

const password = 'greaterthanten';

describe('Status', () => {
    it('should not display user info if user is not logged in', () => {
        cy
            .visit('/status')
            .get('p').contains('You must be logged in to view this')
            .get('a').contains('User Status').should('not.be.visible')
            .get('a').contains('Register')
            .get('a').contains('Log In')
            .get('.notification.is-success').should('not.be.visible')
    });
    it('should display user info if user is logged in', () => {
        // register user
        cy
            .visit('/register')
            .get('input[name="username"]').contains(username)
            .get('input[name="email"]').contains(email)
            .get('input[name="password"]').contains(password)
            .get('input[type="submit"]').click()
        
        cy.wait(400);

        // assert 'status' is display properly
        cy.visit('/status')
        cy.get('.navbar-burger').click()
        cy.contains('User Status').click()
        cy
            .get('li > strong').contains('User Id')
            .get('li > strong').contains('Email: ')
            .get('li').contains('email')
            .get('li > strong').contains('Username')
            .get('li').contains('username')
            .get('a').contains('User Status')
            .get('a').contains('Log Out')
    });
    
});