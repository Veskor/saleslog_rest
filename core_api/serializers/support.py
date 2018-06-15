from rest_framework import serializers
from ..models import Support
from django.contrib.auth.models import User

class SupportSerializer(serializers.ModelSerializer):
    fields = serializers.JSONField()
    class Meta:
        model = Support
        fields = ('id','name','network','fields')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','username')

class AddUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    class Meta:
        fields = ('user_id')
# izlistaj usere u svakom support view !
