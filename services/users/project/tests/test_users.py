# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.api.models import User
from project import db
from project.tests.utils import add_user, add_admin


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
        # user = add_user('test', 'test@test.com', 'test')
        # user = User.query.filter_by(email='test@test.com').first()
        # user.admin=True
        # db.session.commit()
        user = add_admin('test', 'test@test.com', 'test')
        
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            # import pdb; pdb.set_trace()
            response = self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('gamal@gamal.com was added', data['message'])
            self.assertTrue(user.admin)
        

    def test_add_users_invalid_json(self):
        """ Error is thrown if empty json """
        user = add_admin('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/flowers',
                data = json.dumps({}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
        
    def test_add_users_invalid_json_keys(self):
        """ Error is thrown if invalid json keys """
        user = add_admin('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            token = json.loads(resp_login.data.decode())['auth_token']

            response = self.client.post(
                '/flowers',
                data=json.dumps({
                    'email': 'gamal@gamal.com',
                    # 'password': 'hello' # must be non-empty - Weird
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
        
    def test_add_users_duplicate_email(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json',
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com', 
                    'password': 'greaterthaneight'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            response = self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com',
                    'password': 'greaterthaneight'
                }),
                content_type='application/json'
            )

            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('Provide a valid token', data['message'])
        
    """ Test Single User Functionality """
    def test_get_single_user(self):
        """ Ensure single user behaves correctly """
        user = add_user('gamal', 'gamal@gamal.com', 'greaterthaneight')
        # import pdb; pdb.set_trace()
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
        user1 = add_user('laurie', 'laurie@laurie.com', 'greaterthaneight')
        user2 = add_user('gamal', 'gamal@gamal.com', 'greaterthaneight')

        with self.client:
            response = self.client.get('/flowers')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['users']), 2)
            self.assertIn(data['message'], 'success')
        
    
    def test_add_user_inactive(self):
        add_user('test', 'test@test.com', 'test')
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
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com',
                    'password': 'test1234'
                }),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(response.status_code, 403)

    def test_users_is_not_admin(self):
        add_user('test', 'test@test.com', 'test')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data = json.dumps({
                    'email': 'test@test.com',
                    'password': 'test'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/flowers',
                data = json.dumps({
                    'username': 'gamal',
                    'email': 'gamal@gamal.com',
                    'password': 'test1234'
                }),
                content_type='application/json',
                headers = {'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == 'You do not have permission to do that.')
            self.assertEqual(response.status_code, 401)
            

if __name__ == '__main__':
    unittest.main()