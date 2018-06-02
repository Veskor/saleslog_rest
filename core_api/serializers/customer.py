from ..models import Customer, Chain
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):

    data = serializers.JSONField()

    class Meta:
        model = Customer
        fields = ('id',
                  'data',
                  'payment_done')
