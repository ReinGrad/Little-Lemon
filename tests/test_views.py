from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from restaurant.models import Menu


class MenuPermissionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.menu_item = Menu.objects.create(title='IceCream', price='80.00', Inventory=100)
        self.list_url = '/restaurant/menu/'
        self.detail_url = f'/restaurant/menu/{self.menu_item.pk}'

    def test_get_menu_without_token_is_allowed(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_get_menu_with_token_is_allowed(self):
        response = self.client.get(self.list_url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, 200)

    def test_post_menu_without_token_is_denied(self):
        payload = {'title': 'Pizza', 'price': '15.00', 'Inventory': 20}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_post_menu_with_token_is_allowed(self):
        payload = {'title': 'Pasta', 'price': '18.00', 'Inventory': 15}
        response = self.client.post(
            self.list_url,
            payload,
            format='json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, 201)

    def test_put_menu_without_token_is_denied(self):
        payload = {'title': 'Gelato', 'price': '90.00', 'Inventory': 90}
        response = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_put_menu_with_token_is_allowed(self):
        payload = {'title': 'Gelato', 'price': '90.00', 'Inventory': 90}
        response = self.client.put(
            self.detail_url,
            payload,
            format='json',
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_menu_without_token_is_denied(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 401)

    def test_delete_menu_with_token_is_allowed(self):
        response = self.client.delete(self.detail_url, HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.assertEqual(response.status_code, 204)
