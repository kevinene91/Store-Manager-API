import unittest
import json

from .dummy import users, users_login, empty
from .base import BaseTest
"""
    Tests for user auth
"""


class AuthEndpointsTestCase(BaseTest):

    # sucess register
    def test_register(self):
        response = self.client.post('/api/v1/register',
                                    data=json.dumps(users[9]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('registration sucessfull', str(response.data))

    # test with empty data
    def test_register_without_data(self):
        response = self.client.post('/api/v1/register', data=json.dumps(empty),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameter', str(response.data))

    # test already used email
    def test_register_existing_email(self):
        response = self.client.post('/api/v1/register',
                                    data=json.dumps(users[0]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertIn('user with email already registred', str(response.data))

    # test resgister invalid email
    def test_register_invalid_email(self):
        response = self.client.post('/api/v1/register',
                                    data=json.dumps(users[1]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('invalid email', str(response.data))

    # test sucess login
    def test_login(self):
        response = self.client.post('/api/v1/login', data=json.dumps(users[0]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged in', str(response.data))

    # test login without data
    def test_login_without_data(self):
        response = self.client.post('/api/v1/login', data=json.dumps(empty),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameter ', str(response.data))

    # test login invalid email
    def test_login_invalid_email(self):
        response = self.client.post('/api/v1/login', data=json.dumps(users[1]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('invalid email', str(response.data))

    # test login missing email
    def test_login_missing_email(self):
        response = self.client.post('/api/v1/login', data=json.dumps(users[4]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required parameter ', str(response.data))

    # test login missing password
    def test_login_missing_password(self):
        response = self.client.post('/api/v1/login', data=json.dumps(users[5]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        assert 'Missing required parameter ', str(response.data)

    # test login mismatching password
    def test_login_invalid_password(self):
        response = self.client.post('/api/v1/login', data=json.dumps(users[7]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)
        self.assertIn('invalid credentials', str(response.data))

    # test logout
    def test_logout(self):
        response = self.client.post('/api/v1/logout',
                                    headers=self.attendant_headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('logged out', str(response.data))