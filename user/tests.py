from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User


class UserTests(APITestCase):
    user_test_data = {'username': 'test_user', 'password': '123456'}

    def create_account(self, data=None):
        if not data:
            data = self.user_test_data
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        return response

    def get_token(self, data=None):
        if not data:
            data = self.user_test_data
        url = reverse('get_token')
        return self.client.post(url, data, format='json')

    def greet(self, token):
        url = reverse('greet')
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return self.client.get(url)

    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        response = self.create_account()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test_user')

    def test_account_login(self):
        """
        Ensure we can login.
        """
        self.create_account()
        response = self.get_token()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_greet(self):
        """
        Ensure we can call an authorized API
        """
        self.create_account()
        token_resp = self.get_token()
        token = token_resp.data['access']
        response = self.greet(token)
        self.assertContains(response, self.user_test_data['username'])

    def test_block_user(self):
        """
        Ensure we can block users to prevent them login again
        """
        support_user = User('support', permission=User.Permission.SUPPORT)
        support_user.set_password('123456')
        support_user.save()

        self.create_account()
