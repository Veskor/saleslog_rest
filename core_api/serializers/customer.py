from ..models import Customer, Chain

from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):

    data = serializers.JSONField()
    chain = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id',
                  'data',
                  'support',
                  'chain',
                  'payment_done')

    def get_chain(self, obj):
        try:
            return Chain.objects.get(customer=obj.id).id
        except:
            return ''
