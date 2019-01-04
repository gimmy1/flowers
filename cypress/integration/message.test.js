const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;
const password = 'greaterthanten';

describe('Message', () => {
    it('should display flash message correctly', () => {
        // register user
        cy
            .visit('/register')
            .get('input[name=username]').type(username)
            .get('input[name=email]').type(email)
            .get('input[name=password]').type(password)
            .get('input[type="submit"]').click()
        cy
            .get('.notification.is-success').contains('Welcome!')
            .get('delete').click()
            .get('.notification.is-success').should('not.be.visible')
        
            // log a user out
        cy.get('.navbar-burger').click();
        cy.contains('Log Out').click();

        // attempt to log-in
        cy
            .visit('/login')
            .get('input[name="email"]').clear().type(email)
            .get('input[name="password"]').clear().type(password)
            .get('input[type="submit"]').click()
        
        // assert flash message is removed after 3 seconds
        cy
            .get('.notification.is-success').contains('Welcome')
            .wait(4000)
            .get('.notification.is-success').should('not.be.visible')
    })
})
