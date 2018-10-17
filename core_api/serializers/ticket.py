from ..models import Ticket, Chain
from rest_framework import serializers
from .chain import ChainSerializer
from .repair import RepairSerializer

import json

class TicketSerializer(serializers.ModelSerializer):

    info = serializers.JSONField()
#    repair = RepairSerializer()

    class Meta:
        model = Ticket
        fields = ('id','tag','info','repair','support','status')

    def validate_status(self, status):
        if status.status_type.relation.model == 'Support':
            if int(self.initial_data['support']) == status.status_type.relation.model_id:
                return status
        raise serializers.ValidationError("Support id's wrong")
