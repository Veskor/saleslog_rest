from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.factories.user import AdminFactory
import json

from core_api.models import Support, Customer, RepairNetwork
from core_api.factories.support import SupportFactory

from core_api.factories.repair import RepairNetworkFactory

class TestSupport(APITestCase):
    fixtures = ['support.json', 'network.json']
    def setUp(self):
        super(TestSupport, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.network = RepairNetwork.objects.first()
        self.support = Support.objects.first()

    def test_list(self):
        response = self.client.get('/api/v1/support/')
        self.assertGreater(len(response.data), 0)

    def test_create(self):
        data = {
            'name': self.support.name + "new",
            'ip': self.support.ip,
            'network':self.network.id,
            'fields': '{}'
        }
        response = self.client.post('/api/v1/support/',data=data)
        self.assertEqual(response.status_code,200)


    def test_delete(self):
        url = f'/api/v1/support/{self.support.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update(self):
        data = {
            'name':'new_name',
            'fields': json.dumps([{'name':'some_field','type':'Char','args':[]}]),
        }
        url = f'/api/v1/support/{self.support.id}/'
        response = self.client.get(url)
        response.data['support'].update(data)
        del response.data['support']['logo']
        response = self.client.put(url,response.data['support'],format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],data['name'])
        self.assertEqual(response.data['fields'],data['fields'])

    def test_adduser(self):
        pass

    def test_popuser(self):
        pass
