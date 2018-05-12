from ..models import Customer, Chain
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):

    data = serializers.JSONField()

    class Meta:
        model = Customer
        fields = ('id',
                  'data',
                  'payment_done')

    def validate(self, data):
        # Create Chain for every customer
        print(data)
        chain = Chain.objects.create(tickets='',customer=data['id'])
        chain.save()
