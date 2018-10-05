from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core_api.factories.customer import CustomerFactory

from accounts.factories.user import AdminFactory

from core_api.models import Chain

class TestChain(APITestCase):
    def setUp(self):
        super(TestChain, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.customer = CustomerFactory()
        self.customer.save()
        self.chain = Chain.objects.get(customer=self.customer.id)

    def test_get_chains(self):
        response = self.client.get('/api/v1/chain/')
        self.assertGreater(len(response.data), 0)

    def test_get_chain(self):
        url = f'/api/v1/chain/{self.chain.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer']['id'],self.chain.id)
