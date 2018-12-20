from rest_framework import serializers

from accounts.models import User
from lib.utils import validate_email as email_is_valid

from accounts.models import User, USER_TYPES, SALES, \
                            ADMIN, MANAGER, SUPER_ADMIN

from core_api.models import Support

import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name','activation_key')


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name', 'password','user_type', 'groups')

    def get_groups(self, value):
        groups = []
        for item in self.instance.groups.all():
            name, id = item.name.split(':')
            support = Support.objects.get(id=id)

            groups.append({id:support.color})

        return groups
    def create(self, validated_data):
        """
        Create the object.

        :param validated_data: string
        """
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        """
        Validate if email is valid or there is an user using the email.

        :param value: string
        :return: string
        """

        if not email_is_valid(value):
            raise serializers.ValidationError('Please use a different email address provider.')

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already in use, please use a different email address.')

        return value


class CreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    gender = serializers.ChoiceField(choices=User.GENDER_CHOICES)
    user_type = serializers.ChoiceField(choices=USER_TYPES)

    class Meta:
        model = User
        fields = ('email','first_name','last_name','username','gender','user_type')

    def create(self, data):
        if(data['user_type'] == SALES):
            user = User.objects.create_user(email=data['email'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            username=data['username'],
                                            gender=data['gender'],
                                            password='')
            saved = user.save()

        elif(data['user_type'] == ADMIN):
            user = User.objects.create_admin(email=data['email'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            username=data['username'],
                                            gender=data['gender'],
                                            password='')

            saved = user.save()

        elif(data['user_type'] == MANAGER):
            user = User.objects.create_manager(email=data['email'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            username=data['username'],
                                            gender=data['gender'],
                                            password='')

            saved = user.save()

        elif(data['user_type'] == SUPER_ADMIN):

            user = User.objects.create_superuser(email=data['email'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'],
                                            username=data['username'],
                                            gender=data['gender'],
                                            password='')
            saved = user.save()

        # send email with activation_key
        return data

class PasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('password1','password2')

    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        else:
            return data

    def save(self,obj):
        obj.set_password(self.validated_data['password1'])
        obj.save()
