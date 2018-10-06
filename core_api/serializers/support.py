from rest_framework import serializers
from ..models import Support
from django.contrib.auth.models import User

class SupportSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()
    ip = serializers.IPAddressField()
    class Meta:
        model = Support
        fields = ('id','name','network','fields','ip')

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
