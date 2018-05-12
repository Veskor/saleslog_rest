from rest_framework import viewsets

from ..serializers.chain import ChainSerializer
from ..serializers.customer import CustomerSerializer
from ..serializers.ticket import TicketSerializer

from ..models import Customer, Ticket

class ChainViewset(viewsets.ModelViewSet):
    serializer_class = ChainSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def get(self,request,pk=None):
        print('hi')
        try:
            chain = self.get_object()
            chain = ChainSerializer(chain)

            customer = Customer.objects.get(pk=pk)
            customer = CustomerSerializer(customer)

            tickets = []
            for item in chain['tickets']:
                tickets.append(Ticket.objects.get(pk=item))
            tickets = TicketSerializer(tickets,many=True)
        except Exception as e:
            print(e)
            return Response({'error':'Invalid chain id'})
        return Response({'customer': customer.data,
                        'tickets': tickets.data,
                        })
