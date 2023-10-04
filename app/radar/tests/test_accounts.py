from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.radar.models import InstagramAccount
from app.radar.tests import authenticate, ACCOUNT_DATA_1, IG_ACCESS_TOKEN_1, IG_ID, ACCOUNT_DATA_2, \
    init_ig_account


class InstagramAccountsTestCase(APITestCase):
    list_url = reverse('ig-account-list')

    @authenticate
    def test_create(self, user):
        response = self.client.post(self.list_url, ACCOUNT_DATA_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InstagramAccount.objects.count(), 1)
        response_data = response.json()
        self.assertEqual(response_data['user'], user.id)
        self.assertEqual(response_data['ig_id'], IG_ID)
        self.assertEqual(response_data['access_token'], IG_ACCESS_TOKEN_1)
        InstagramAccount.objects.get(user = user).delete()

    @authenticate
    @init_ig_account
    def test_create_existing_token(self, user):
        response = self.client.post(self.list_url, ACCOUNT_DATA_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("instagram account with this access token already exists.", response.json()['access_token'])

    @authenticate
    @init_ig_account
    def test_create_existing_ig_id(self, user):
        response = self.client.post(self.list_url, ACCOUNT_DATA_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_unauthorized(self):
        response = self.client.post(self.list_url, ACCOUNT_DATA_1, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @authenticate
    @init_ig_account
    def test_list(self, user):
        response = self.client.get(self.list_url, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['user'], user.id)
        self.assertEqual(response_data[0]['ig_id'], IG_ID)
        self.assertEqual(response_data[0]['access_token'], IG_ACCESS_TOKEN_1)

    @authenticate
    @init_ig_account
    def test_patch_access_token(self, user):
        detail_url = reverse('ig-account-detail', kwargs = {'pk': user.ig_accounts.first().id})
        response = self.client.patch(detail_url, ACCOUNT_DATA_2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['access_token'], ACCOUNT_DATA_2['access_token'])
