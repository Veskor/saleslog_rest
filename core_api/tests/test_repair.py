from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.test import TestCase

from accounts.factories.user import AdminFactory

from core_api.factories.repair import RepairNetworkFactory, RepairFactory,\
                                      PartFactory, EquipmentFactory, EngineerFactory
from core_api.models import RepairNetwork, Repair

class TestRepair(APITestCase):

    def setUp(self):
        super(TestRepair, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.repair = RepairFactory()
        self.repair.save()
        self.part = PartFactory()
        self.part.save()
        self.engineer = EngineerFactory()
        self.engineer.save()
        self.equipment = EquipmentFactory()
        self.equipment.save()

    def test_list(self):
        response = self.client.get(f'/api/v1/network/{self.repair.network.id}/repair/')
        self.assertGreater(len(response.data), 0)

    def test_create(self):
        data = {
            'part':self.part.id,
            'equipment':self.equipment.id,
            'engineer':self.engineer.id
        }
        response = self.client.post(f'/api/v1/network/{self.repair.network.id}/repair/',\
                                    data=data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(data['part'],response.data['part'])
        self.assertEqual(data['equipment'],response.data['equipment'])
        self.assertEqual(data['engineer'],response.data['engineer'])

    def test_delete(self):
        url = f'/api/v1/network/{self.repair.network.id}/repair/{self.repair.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_update(self):

        data = {
            'part':self.part.id,
            'equipment':self.equipment.id,
            'engineer':self.engineer.id
        }

        url = f'/api/v1/network/{self.repair.network.id}/repair/{self.repair.id}/'
        response = self.client.get(url)
        response.data.update(data)
        response = self.client.put(url,response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['part'],response.data['part'])
        self.assertEqual(data['equipment'],response.data['equipment'])
        self.assertEqual(data['engineer'],response.data['engineer'])

class TestRepairNetwork(APITestCase):
    fixtures = ['network.json']
    def setUp(self):
        super(TestRepairNetwork, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.repair_network = RepairNetworkFactory()

    def test_list(self):
        response = self.client.get('/api/v1/network/')
        self.assertGreater(len(response.data),0)

    def test_create(self):
        data = {
            'name': 'some random network 1',
        }
        response = self.client.post('/api/v1/network/',data=data)
        self.assertEqual(response.data['name'],data['name'])
        self.assertEqual(response.status_code,200)

    def test_update(self):
        data = {
            'name': 'some random network 2',
        }
        url = f'/api/v1/network/{self.repair_network.id}/'
        response = self.client.get(url)
        response.data.update(data)
        response = self.client.put(url,response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],data['name'])

    def test_delete(self):
        url = f'/api/v1/network/{self.repair_network.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
