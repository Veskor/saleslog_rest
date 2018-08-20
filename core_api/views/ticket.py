from ..serializers.ticket import TicketSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import viewsets

class TicketViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = serializer_class.Meta.model.objects.all()

#    def create(self,request):
#        print(request.POST[''])
#        return Response({'vex':'car'})
