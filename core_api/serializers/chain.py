from ..models import Chain, Status
from rest_framework import serializers

class ChainSerializer(serializers.ModelSerializer):

    tickets = serializers.JSONField()
    statuses = serializers.JSONField()
    class Meta:
        model = Chain
        fields = ('id','tickets','statuses','customer')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name','color')
