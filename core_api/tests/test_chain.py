from django.urls import reverse
from rest_framework.test import APITestCase

from accounts.factories.user import AdminFactory

from core_api.models import Chain, Customer

class TestChain(APITestCase):
    fixtures = ['customer.json','support.json','network.json']

    def setUp(self):
        super(TestChain, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.customer = Customer.objects.first()
        self.chain = Chain.objects.get(customer=self.customer.id)

    def test_get_chains(self):
        response = self.client.get('/api/v1/chain/')
        self.assertGreater(len(response.data), 0)

    def test_get_chain(self):
        url = f'/api/v1/chain/{self.chain.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer']['id'],self.chain.id)
