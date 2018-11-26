# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.api.models import User
from project import db

def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /flowers/flower route behaves correctly."""
        response = self.client.get('/flowers/flower')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('soon', data['flower'])
    
    """ Test Add User Functionality """
    def test_add_users(self):
        with self.client:
            response = self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('gamal@gamal.com was added', data['message'])
        

    def test_add_users_invalid_json(self):
        """ Error is thrown if empty json """
        with self.client:
            response = self.client.post(
                '/flowers',
                data = json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
        
    def test_add_users_invalid_json_keys(self):
        """ Error is thrown if invalid json keys """
        with self.client:
            response = self.client.post(
                '/flowers',
                data=json.dumps({
                    'email': 'gamal@gamal.com'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
        
    def test_add_users_duplicate_email(self):
        with self.client:
            self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com'
                }),
                content_type='application/json'
            )
            response = self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com'
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. That email already exists', data['message'])
        
    """ Test Single User Functionality """
    def test_get_single_user(self):
        """ Ensure single user behaves correctly """
        user = add_user('gamal', 'gamal@gamal.com')
        import pdb; pdb.set_trace()
        with self.client:
            response = self.client.get(f'/flowers/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('gamal@gamal.com exists', data['message'])
        
    def test_single_user_no_id(self):
        """ Error is thrown if id not provided """
        response = self.client.get(f'/flowers/blah')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not exist', data['message'])
    
    def test_single_user_incorrect_id(self):
        """ Ensure error is thrown if incorrect id is provided """
        response = self.client.get('flowers/888')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertIn('User does not exist', data['message'])

    """ Test Get All Users Functionality """
    def test_all_users(self):
        user1 = add_user('laurie', 'laurie@laurie.com')
        user2 = add_user('gamal', 'gamal@gamal.com')

        with self.client:
            response = self.client.get('/flowers')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn(data['message'], 'success')
        
    
    # def test_


if __name__ == '__main__':
    unittest.main()