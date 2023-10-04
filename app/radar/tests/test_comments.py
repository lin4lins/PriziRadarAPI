from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from app.radar.models import InstagramPost
from app.radar.tests import authenticate, init_ig_account, POST_URL, POST_NO_COMMENTS_URL


class InstagramAccountsTestCase(APITestCase):
    url = reverse('random-comment')

    @authenticate
    @init_ig_account
    def test_get_random_comment(self, user):
        ig_account_id = user.ig_accounts.first().id
        post_data = {'url': POST_URL, 'account_id': ig_account_id}
        response = self.client.post(self.url, post_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        InstagramPost.objects.get(url=POST_URL).delete()

    @authenticate
    @init_ig_account
    def test_get_no_comments(self, user):
        ig_account_id = user.ig_accounts.first().id
        post_data = {'url': POST_NO_COMMENTS_URL, 'account_id': ig_account_id}
        response = self.client.post(self.url, post_data, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertIn('warning', response_data)
        self.assertEqual(response.json()['warning'], 'No comments found')
        InstagramPost.objects.get(url = POST_NO_COMMENTS_URL).delete()
