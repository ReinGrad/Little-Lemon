from django.contrib.auth.models import User
from django.test import TestCase

from restaurant.models import Menu


class AIInstrumantelViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='secret123')

    def test_requires_authentication(self):
        response = self.client.get('/restaurant/ai-instrumantel/')
        self.assertEqual(response.status_code, 403)

    def test_returns_menu_insights(self):
        Menu.objects.create(title='Pasta', price=20, Inventory=10)
        Menu.objects.create(title='Steak', price=40, Inventory=5)

        self.client.login(username='tester', password='secret123')
        response = self.client.get('/restaurant/ai-instrumantel/')

        self.assertEqual(response.status_code, 200)
        body = response.json()

        self.assertEqual(body['feature'], 'ai-instrumantel')
        self.assertEqual(body['total_items'], 2)
        self.assertIn('recommendation', body)
        self.assertEqual(float(body['average_price']), 30.0)
