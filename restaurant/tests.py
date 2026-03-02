from django.test import TestCase
from rest_framework.test import APIClient

from restaurant.models import Menu


class AIHelperViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        Menu.objects.create(title='Salad', price='6.50', Inventory=10)
        Menu.objects.create(title='Pasta', price='12.00', Inventory=8)
        Menu.objects.create(title='Steak', price='24.00', Inventory=5)

    def test_ai_helper_requires_prompt(self):
        response = self.client.post('/restaurant/ai-helper/', data={}, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('detail', response.json())

    def test_ai_helper_returns_budget_recommendations(self):
        response = self.client.post(
            '/restaurant/ai-helper/',
            data={'prompt': 'Can you suggest affordable dishes?'},
            format='json',
        )

        payload = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload['reply'], 'Here are the most affordable menu items.')
        self.assertEqual(payload['suggestions'][0], 'Salad ($6.50)')
