from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route


from accounts.models import User, USER_TYPES, SALES, \
                            ADMIN, MANAGER, SUPER_ADMIN
from accounts.serializers import UserRegistrationSerializer, UserSerializer
from lib.utils import AtomicMixin

# create every type of user
# login with jwt (obtain jwt)

from rest_framework import serializers

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
            print('hey')
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
                                            password='vexadija')
            saved = user.save()

        # send email with activation_key
        print(user.username)
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
        print(data['password2'])
        if data['password1'] == data['password2']:
            # set password
            pass
        else:
            return False

class UserCreationView(viewsets.ViewSet):
    serializer_class = CreateSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self,request):
        users = User.objects.all()
        users = self.serializer_class(users,many=True)
        return Response({"users":users.data})

    def create(self,request):

        data = self.serializer_class(data=request.data)
        data.is_valid()

        data.save()

        user_created = data.data

        return Response({'user':user_created})

class ConfrmUser(viewsets.ViewSet):
    serializer_class = PasswordSerializer
    @detail_route(methods=['post'])
    def SetPassword(self, request, pk=None):
        data = self.serializer_class(data=request.data)
        return Response({'error': data.is_valid()})

class Login():
    def obtain_token():
        pass
