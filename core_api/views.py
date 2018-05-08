from django.shortcuts import get_object_or_404
from django_rest_logger import log
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from accounts.models import User
from .serializers import *
from lib.utils import AtomicMixin

# Create your views here.
class CustomerViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()

class RepairNetworkViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = RepairNetworkSerializer
    queryset = serializer_class.Meta.model.objects.all()

class SupportViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = SupportSerializer
    queryset = serializer_class.Meta.model.objects.all()
