from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core_api.factories.ticket import TicketFactory
from core_api.factories.customer import CustomerFactory
from core_api.factories.support import SupportFactory
from core_api.factories.repair import RepairFactory
from accounts.factories.user import AdminFactory

from core_api.models import Ticket, Chain, Status, StatusType, Customer

import json

class TestTicket(APITestCase):
    def setUp(self):
        super(TestTicket, self).setUp()
        self.admin = AdminFactory()
        self.client.force_authenticate(user=self.admin)
        self.admin.save()
        self.support = SupportFactory()
        self.support.save()
        self.customer = Customer.objects.create(data="{}",
                                                support=self.support,
                                                payment_done=True)
        self.customer.save()
        self.chain = Chain.objects.get(customer=self.customer.id)
        self.status_type = StatusType.objects\
                                     .filter(relation__model='Support',
                                             relation__model_id=self.support.id,
                                             )[0]
        self.status = Status.objects.create(name='Test Status',
                                            color='White',
                                            status_type=self.status_type)
        self.status.save()
        self.repair = RepairFactory()
        self.repair.save()
        self.ticket = Ticket.objects.create(tag=self.chain,
                                            info=json.dumps({'example':'ticket'}),
                                            support=self.support,
                                            status=self.status,
                                            repair=self.repair,
                                            )
        self.ticket.save()

    def test_list(self):
        response = self.client.get('/api/v1/ticket/')
        self.assertGreater(len(response.data), 0)

    def test_create(self):
        data = {
            'tag': self.chain.id,
            'info': json.dumps({'example':'ticket'}),
            'support': self.support.id,
        }
        response = self.client.post('/api/v1/ticket/', data)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_delete(self):
        url = f'/api/v1/ticket/{self.ticket.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code,204)

    def test_update(self):
        data = {
            'info': json.dumps({'some stuff changed':'for good'}),
        }
        url = f'/api/v1/ticket/{self.ticket.id}/'
        response = self.client.get(url)
        response.data.update(data)
        response = self.client.put(url,response.data)
        self.assertEqual(response.status_code, 200)
