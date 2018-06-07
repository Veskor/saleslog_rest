from rest_framework import viewsets
from rest_framework.response import Response
from ..serializers.support import SupportSerializer
from ..serializers.ticket import TicketSerializer
from ..models import Ticket

class SupportViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = SupportSerializer
    queryset = serializer_class.Meta.model.objects.all()


    def retrieve(self,request,pk=None):

        tickets = Ticket.objects.filter(support=pk)
        tickets = TicketSerializer(tickets,many=True)

        support = SupportSerializer(self.get_object())

        return Response({'support': support.data,
                         'tickets': tickets.data,
                         })
