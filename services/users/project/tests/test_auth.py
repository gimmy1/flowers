import json
from flask import current_app
# import time

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = self.client.post(
                '/auth/register',
                data = json.dumps({
                    'username': 'testwithlaurie',
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }), 
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'success')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.status_code, 201)

    
    def test_user_registration_duplicate_email(self):
        user = add_user('testwithlaurie', 'laurie@laurie.com', 'password123')
        with self.client:
            response = self.client.post(
                'auth/register',
                data = json.dumps({
                    'username': 'testwithgamal',
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry that user already exists.', data['message'])

        
    def test_user_registration_duplicate_username(self):
        user = add_user('testwithlaurie', 'laurie@laurie.com', 'password123')
        with self.client:
            response = self.client.post(
                'auth/register', 
                data = json.dumps({
                    'username': 'testwithlaurie',
                    'email': 'laurie@lauri2e.com',
                    'password': '1234'
                }),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry that user already exists.', data['message'])

    def test_user_registration_invalid_json(self):
        with self.client: 
            response = self.client.post(
                'auth/register', 
                data = json.dumps({}),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])

        
    def test_user_registrationj_invalid_json_keys_no_username(self):
        with self.client:
            response = self.client.post(
                'auth/register',
                data = json.dumps({
                    'email': 'laurie@lauri2e.com',
                    'password': '1234'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
        
    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            response = self.client.post(
                'auth/register',
                data = json.dumps({
                    'username': 'testwithlaurie',
                    'password': '1234'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
        
    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            response = self.client.post(
                'auth/register',
                data = json.dumps({
                    'username': 'testwithlaurie',
                    'email': 'laurie@laurie'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
        
    
    def test_registered_user_login(self):
        with self.client:
            add_user('testwithlaurie', 'laurie@laurie.com', 'password123')
            response = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }),
                content_type = 'application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'logout success')
            self.assertTrue(data['message'] == 'logout success')
            self.assertTrue(data['auth_token'])
            self.assertEqual(response.status_code, 200)
        
    def test_not_registered_user_login(self):
        with self.client:
            response = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(data['status'], 'fail')
            self.assertTrue(data['message'] == 'User does not exist.')
            self.assertEqual(response.status_code, 404)
        
    def test_valid_logout(self):
        add_user('testwithlaurie', 'laurie@laurie.com', 'password123')
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers = {'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Succcessful')
            self.assertEqual(response.status_code, 200)

        
    def test_invalid_logout_expired_token(self):
        add_user('testwithlaurie', 'laurie@laurie.com', 'password123')
        current_app.config['TOKEN_EXPIRATION_SECONDS'] = -1
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }),
                content_type='application/json'
            )
            # invalid token output
            # time.sleep(4)
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Signature expired. Please log in again')
            self.assertEqual(response.status_code, 401)


    def test_invalid_logout(self):
        with self.client:
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer invalid.'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please try again.')
            self.assertEqual(response.status_code, 401)
        
    def test_user_status(self):
        add_user('testwithlaurie', 'laurie@laurie.com', 'password123')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'laurie@laurie.com',
                    'password': 'password123'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data']['email'] == 'laurie@laurie.com')
            self.assertTrue(data['data']['active'])
            self.assertFalse(data['data']['admin'])
        
    def test_invalid_status(self):
        with self.client:
            response = self.client.get(
                '/auth/status',
                headers = {'Authorization': f'Bearer invalid'}
            )
            data = json.loads(response.data.decode())
            # import pdb; pdb.set_trace()
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Invalid token. Please try again.')
            self.assertEqual(response.status_code, 401)

    def test_invalid_logout_inactive(self):
        add_user('test', 'test@test.com','test')
        #update user
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token=json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(response.status_code, 401)
        
    def test_invalid_status_inactive(self):
        # update user
        add_user('test', 'test@test.com', 'test')
        user = User.query.filter_by(email='test@test.com').first()
        user.active = False
        db.session.commit()
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token=json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(response.status_code, 401)
