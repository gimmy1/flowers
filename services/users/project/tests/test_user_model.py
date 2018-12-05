import unittest
from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
from project.tests.utils import add_user

from sqlalchemy.exc import IntegrityError

class TestUserModel(BaseTestCase):
    def test_add_user(self):
        user = add_user('lauriestest', 'laurie@laurie.com', 'greaterthaneight')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'lauriestest')
        self.assertEqual(user.email, 'laurie@laurie.com')
        self.assertTrue(user.active)

        
    def test_add_user_duplicate_username(self):
            user = add_user('lauriestest', 'laurie@laurie.com', 'greaterthaneight')
            duplicate_user = User(
                username='lauriestest',
                email='laurie@laurie2.com', 
                password='greaterthaneight'
            )
            db.session.add(duplicate_user)
            self.assertRaises(IntegrityError, db.session.commit)

        
    def test_add_user_duplicate_email(self):
        user = add_user('lauriestest', 'laurie@laurie.com', 'greaterthaneight')
        duplicate_user = User(
            username='lauriestest2',
            email='laurie@laurie.com',
            password='greaterthaneight'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    
    def test_to_json(self):
        user = add_user('lauriestest', 'laurie@laurie.com', 'greaterthaneight')
        self.assertTrue(isinstance(user.to_json(), dict))
    
    def test_password_are_random(self):
        user_one = add_user('lauriestest','laurie@laurie.com', 'greaterthaneight')
        user_two = add_user('lauriestest2','laurie@laurie2.com', 'greaterthaneight')
        self.assertNotEqual(user_one.password, user_two.password)
        


if __name__ == '__main__':
    unittest.main()
