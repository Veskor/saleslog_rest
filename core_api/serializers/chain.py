from ..models import Chain
from rest_framework import serializers

class ChainSerializer(serializers.ModelSerializer):

    tickets = serializers.ListField(
        child=serializers.CharField()
        )

    class Meta:
        model = Chain
        fields = ('id','tickets','customer')
