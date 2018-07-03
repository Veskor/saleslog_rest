from django.shortcuts import get_object_or_404
from django.contrib.auth.models import  Group

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from ..serializers.support import SupportSerializer, UserSerializer, AddUserSerializer
from ..serializers.ticket import TicketSerializer
from ..models import Ticket, Support
from accounts.models import User

class SupportViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = SupportSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def get_serializer_class(self):
        if self.action == 'AddUser' or self.action == 'PopUser':
            return AddUserSerializer
        return SupportSerializer

    def retrieve(self,request,pk=None):

        tickets = Ticket.objects.filter(support=pk)
        tickets = TicketSerializer(tickets,many=True)

        support = SupportSerializer(self.get_object())

        group = Group.objects.filter(name=support.data['name'])[0]
        users = User.objects.filter(groups=group.id)
        users = UserSerializer(users,many=True)

        return Response({'support': support.data,
                         'tickets': tickets.data,
                         'users': users.data
                         })

    @detail_route(methods=['post','get'])
    def AddUser(self, request, pk=None):
        if request.method == 'GET':
            users = User.objects.all()
            users = UserSerializer(users,many=True)
            return Response({"users":users.data})
        else:
            support = get_object_or_404(Support, pk=pk)
            group = get_object_or_404(Group, name=support.name)
            user = get_object_or_404(User,pk=request.data['user_id'])
            group.user_set.add(user)
            return Response({'id':request.data['user_id']})

    @detail_route(methods=['post','get'])
    def PopUser(self, request, pk=None):
        self.serializer_class = AddUserSerializer
        if request.method == 'GET':
            users = User.objects.all()
            users = UserSerializer(users,many=True)
            return Response({"users":users.data})
        else:
            support = get_object_or_404(Support, pk=pk)
            group = get_object_or_404(Group, name=support.name)
            user = get_object_or_404(User,pk=request.data['user_id'])
            group.user_set.remove(user)
            return Response({'id':request.data['user_id']})
