import json

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
            # import pdb; pdb.set_trace()
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
        
    
    # def test_user_registration



