from rest_framework import serializers
from ..models import Support

class SupportSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()
    class Meta:
        model = Support
        fields = ('id','name','network','fields')
