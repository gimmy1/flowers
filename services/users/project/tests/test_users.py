# services/users/project/tests/test_users.py


import json
import unittest

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /flowers/flower route behaves correctly."""
        response = self.client.get('/flowers/flower')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('soon', data['flower'])


if __name__ == '__main__':
    unittest.main()