from rest_framework import viewsets
from rest_framework.response import Response

from ..serializers.chain import ChainSerializer, StatusSerializer, ChatSerializer, MessageSerializer
from ..serializers.customer import CustomerSerializer
from ..serializers.ticket import TicketSerializer

from ..models import Customer, Ticket, Status

import json

class ChainViewset(viewsets.ModelViewSet):
    serializer_class = ChainSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def retrieve(self,request,pk=None):
        try:
            # Get chain
            chain = self.get_object()
            chain = ChainSerializer(chain)

            # Get customer
            customer = Customer.objects.get(pk=pk)
            customer = CustomerSerializer(customer)

            # Get tickets
            tickets = []
            for item in json.loads(chain['tickets'].value):
                tickets.append(Ticket.objects.get(pk=item))
            tickets = TicketSerializer(tickets,many=True)

            # Get statuses
            statuses = []
            for item in json.loads(chain['statuses'].value):
                statuses.append(Status.objects.get(pk=item))
            statuses = StatusSerializer(statuses,many=True)

        except Exception as e:
            print(e)
            return Response({'error':'Invalid chain id'})
        return Response({'customer': customer.data,
                         'tickets': tickets.data,
                         'statuses': statuses.data,
                        })

class StatusViewSet(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    queryset = serializer_class.Meta.model.objects.all()

class ChatsViewSet(viewsets.ModelViewSet):
    serializer_class = ChatSerializer
    queryset = serializer_class.Meta.model.objects.all()

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self,request):
        return Response({'error':'403 FORBIDDEN'})
