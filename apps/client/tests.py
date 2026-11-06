from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Client


class ClientApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('alice', password='secret-pass-123')
        self.other = User.objects.create_user('bob', password='secret-pass-123')
        Client.objects.create(name='Client Alice', email='a@example.test', created_by=self.user)
        Client.objects.create(name='Client Bob', email='b@example.test', created_by=self.other)

    def test_list_requires_authentication(self):
        response = self.client.get('/api/v1/clients/')
        self.assertEqual(response.status_code, 401)

    def test_list_only_returns_own_clients(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/v1/clients/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([c['name'] for c in response.json()], ['Client Alice'])

    def test_cannot_read_another_users_client(self):
        other_client = Client.objects.get(created_by=self.other)
        self.client.force_authenticate(self.user)
        response = self.client.get(f'/api/v1/clients/{other_client.pk}/')
        self.assertEqual(response.status_code, 404)

    def test_create_assigns_current_user(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/api/v1/clients/', {'name': 'Nouveau', 'email': 'n@example.test'}, format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Client.objects.get(name='Nouveau').created_by, self.user)
