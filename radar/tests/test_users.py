from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from radar.models import User
from radar.tests import USER_DATA, authenticate


class UsersTestCase(APITestCase):
    list_url = reverse('user-list')

    def test_create(self):
        response = self.client.post(self.list_url, USER_DATA, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, USER_DATA['email'])
        response_data = response.json()
        self.assertIn("token", response_data)
        token = response_data.get("token")
        self.assertIsNotNone(token)
        User.objects.get(email = USER_DATA['email']).delete()

    def test_create_existing_email(self):
        user_1 = User.objects.create(**USER_DATA)
        response = self.client.post(self.list_url, USER_DATA, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this email already exists.", response.json()['email'])
        user_1.delete()

    @authenticate
    def test_retrieve(self, user: User):
        detail_url = reverse('user-detail', kwargs = {'pk': user.id})
        response = self.client.get(detail_url, format = 'json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['id'], user.id)
        self.assertEqual(response_data['email'], user.email)

    def test_retrieve_unauthorized(self):
        detail_url = reverse('user-detail', kwargs = {'pk': 4})
        response = self.client.get(detail_url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @authenticate
    def test_list(self, user: User):
        response = self.client.get(self.list_url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @authenticate
    def test_update(self, user: User):
        detail_url = reverse('user-detail', kwargs = {'pk': user.id})
        updated_data = {
            'email': 'newemail@example.com',
            'password': 'newpassword',
        }
        response = self.client.put(detail_url, updated_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @authenticate
    def test_delete(self, user: User):
        detail_url = reverse('user-detail', kwargs = {'pk': user.id})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
