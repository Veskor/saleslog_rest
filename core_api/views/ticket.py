from ..serializers.ticket import TicketSerializer

from rest_framework import viewsets

class TicketViewset(viewsets.ModelViewSet):
    #    authentication_classes = (TokenAuthentication,)
    #    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = serializer_class.Meta.model.objects.all()
