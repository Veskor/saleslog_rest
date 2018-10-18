from rest_framework import serializers
from ..models import Support, StatusType
from django.contrib.auth.models import User

class SupportSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()
    ip = serializers.IPAddressField()
    status_type = serializers.SerializerMethodField()

    class Meta:
        model = Support
        fields = ('id','name','network','fields','ip','status_type')

    def get_status_type(self, obj):
        return StatusType.objects.get(relation__model='Support',relation__model_id=obj.id).id

class UserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ('id','email','username')

class AddUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    class Meta:
        fields = ('user_id')
