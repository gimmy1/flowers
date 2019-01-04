const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`;

const password = 'greaterthanten';

describe('Login', () => {
    it('should display login form', () => {
        cy
            .visit('/login')
            .get('h1').contains('Login')
            .get('form')
            .get('input[disabled]')
            .get('.validation-list')
            .get('.validation-list > .error').first().contains(
                'Email is required.'
            )
    });
    it('should allow a user to sign in', () => {
        // register user
        cy
            .visit('/register')
            .get('input[name="username"]').type(username)
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('test')
            .get('input[type="submit"]').click()
            console.log('yes')
        
        // log user out
        // cy.get('.navbar-burger').click()
        // cy.contains('Log Out').click()

        // Log user in
        cy
            .get('a').contains('Log In').click()
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('test')
            .get('input[type="submit"]').click()
            .wait(100);
        
        // assert user is redirected to /
        cy.contains('All Users')
        cy
            .get('table')
            .find('tbody > tr').last()
            .find('td').contains(username);
        
        // log user out
        cy
            .get('a').contains('Log Out').click();
        
        // assert log out is displayed properly
        cy.get('p').contains('You are now logged out.')
        cy.get('.navbar-burger').click();
        cy.contains('All Users');
        cy
            .get('table')
            .find('tbody > tr').last()
            .find('td').contains(username)
        cy.get('.notification.is-success').contains('Welcome!')


        cy
            .get('.navbar-item').contains('User Status').should('not.be.visible')
            // .get('.navbar-item').contains('Log In')
    });
    it('shold throw an error if credentials are incorrect', () => {
        cy
            .visit('/login')
            .get('input[name="email"]').type('incorrect@email.com')
            .get('input[name="password"]').type(password)
            .get('input[type="submit"]').click()
        
        // assert user login failed
        cy.contains('All Users').should('not.be.visible')
        cy.contains('Login')
        cy.get('.navbar-burger').click()
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('Log Out').should('not.be.visible')
                .get('.navbar-item').contains('User Status').should('.not.be.visible')
                .get('.navbar-item').contains('Log In')
                .get('.navbar-item').contains('Register')
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('That user already exists.')
        
        // Attempt to login
        cy
            .get('a').contains('Login')
            .get('input[name="email"]').type(email)
            .get('input[name="password"]').type('incorrectpassword')
            .get('input[type="submit"]').click()
            .wait(100);
        cy.contains('All Users').should('not.be.visible')
        cy.contains('Login')
        cy.get('.navbar-burger').click()
        cy.get('.navbar-menu').within(() => {
            cy
                .get('.navbar-item').contains('User Status').should('not.be.visible')
                .get('.navbar-item').contains('Log Out').should('.not.be.visible')
                .get('.navbar-item').contains('Log In')
                .get('.navbar-item').contains('Register')
        });
        cy
            .get('.notification.is-success').should('not.be.visible')
            .get('.notification.is-danger').contains('That user already exists.')
    });
})

