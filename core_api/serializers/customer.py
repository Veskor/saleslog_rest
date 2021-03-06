from ..models import Customer, Chain, Status, StatusType
from ..serializers.chain import StatusSerializer
from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    class Meta:
        fields = ('file')

class CustomerSerializer(serializers.ModelSerializer):

    data = serializers.JSONField()
    extra_data = serializers.JSONField(required=False)
    chain = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = ('id',
                  'data',
                  'extra_data',
                  'support',
                  'chain',
                  'payment_done')

    def get_chain(self, obj):
        try:
            return Chain.objects.get(customer=obj.id).id
        except:
            return ''

class StatusCustomerSerializer(serializers.Serializer):

    statuses = []

    try:
        for item in Status.objects.all():
            statuses.append((item.id,item.name))
    except:
        pass

    id = serializers.ChoiceField(choices=statuses,allow_blank=True)
    status = StatusSerializer()

class StatusCustomerDeleteSerializer(serializers.Serializer):

    statuses = []

    try:
        for item in Status.objects.all():
            statuses.append((item.id,item.name))
    except:
        pass

    id = serializers.ChoiceField(choices=statuses,allow_blank=True)
