from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):
    user_test_data = {'username': 'test_user', 'password': '123456'}

    def create_account(self, data):
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        return response

    def get_token(self, data):
        url = reverse('get_token')
        return self.client.post(url, data, format='json')

    def greet(self, token):
        url = reverse('greet')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return self.client.get(url)

    def block_user(self, username, support_token):
        url = reverse('block')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {support_token}")
        return self.client.delete(url, dict(username=username), format='json')

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        response = self.create_account(self.user_test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_user')

    def test_account_login(self):
        """
        Ensure we can login.
        """
        self.create_account(self.user_test_data)
        response = self.get_token(self.user_test_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_greet(self):
        """
        Ensure we can call an authorized API
        """
        self.create_account(self.user_test_data)
        token_resp = self.get_token(self.user_test_data)
        token = token_resp.data['access']
        response = self.greet(token)
        self.assertContains(response, self.user_test_data['username'])

    def test_block_user(self):
        """
        Ensure we can block users to prevent them login again
        """

        # create support user
        support_user = User(username='support', permission=User.Permission.SUPPORT)
        support_user.set_password('123456')
        support_user.save()

        # login support user
        token_resp = self.get_token(data=dict(username='support', password='123456'))
        token = token_resp.data['access']

        # create account to block
        self.create_account(self.user_test_data)

        # block account
        response = self.block_user(self.user_test_data['username'], token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ensure that blocked user can't login
        response = self.get_token(self.user_test_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


