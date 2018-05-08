from .models import *
from rest_framework import serializers

class RepairNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairNetwork
        fields = ('id','name')

class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = ('id','name','network')

class CustomerSerializer(serializers.ModelSerializer):
    data = serializers.JSONField()
    class Meta:
        model = Customer
        fields = ('id',
                  'data',
                  'payment_done',
                  'support')

    def validate_data(self, value):
        # add logic 
        print(value)
        return value
