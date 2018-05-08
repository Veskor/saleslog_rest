from models import *
from rest_framework import serializers

class RepairNetworkSerializer(serializers.Serializer):
    class Meta:
        model = RepairNetwork
        fields = ('id','name')

class SupportSerializer(serializers.Serializer):
    class Meta:
        model = Support
        fields = ('id','name','network')

class CustomerSerializer(serializers.Serializer):
    data = serializers.JSONField()
    class Meta:
        model = Customer
        fields = ('id',
                  'data',
                  'payment_done',
                  'support')
