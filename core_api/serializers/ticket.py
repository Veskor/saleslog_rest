from ..models import Ticket, Chain
from rest_framework import serializers
from .chain import ChainSerializer
from .repair import RepairSerializer

class TicketSerializer(serializers.ModelSerializer):

    info = serializers.JSONField()
    repair = RepairSerializer()

    class Meta:
        model = Ticket
        fields = ('id','tag','info','repair','support')
