from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core_api.views.customer import *
from core_api.factories.customer import CustomerFactory
from core_api.factories.support import SupportFactory

from accounts.factories.user import AdminFactory

class TestCustomer(APITestCase):
    def setUp(self):
        super(TestCustomer, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.admin.save()
        self.customer = CustomerFactory()
        self.customer.save()
        self.support = SupportFactory()

    def test_create_customer(self):
        data = {
            "data": "{\"key\":\"value\"}",
            "support": self.support.id,
            "payment_done": True
        }

        response = self.client.post('/api/v1/customer/', data)
        chain = Chain.objects.filter(customer=response.data['chain'])
        self.assertNotEqual(chain,[])
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_list_customers(self):
        response = self.client.get('/api/v1/customer/')
        self.assertGreater(len(response.data), 0)

    def test_delete_customer(self):
        url = f'/api/v1/customer/{self.customer.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update_customer(self):

        data = {
            "payment_done": False,
            "support": self.support.id
        }
        url = f'/api/v1/customer/{self.customer.id}/'
        response = self.client.get(url)
        response.data.update(data)
        response = self.client.put(url,response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['payment_done'],data['payment_done'])
