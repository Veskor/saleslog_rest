from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from ..serializers.ticket import TicketSerializer
from ..pagination import LargeResultsSetPagination

class TicketViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TicketSerializer
    queryset = serializer_class.Meta.model.objects.all()
    pagination_class = LargeResultsSetPagination
