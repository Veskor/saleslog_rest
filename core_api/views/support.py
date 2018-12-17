from django.shortcuts import get_object_or_404
from django.contrib.auth.models import  Group

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from ..serializers.support import SupportSerializer, UserSerializer, AddUserSerializer
from ..serializers.ticket import TicketSerializer
from ..models import Ticket, Support, Customer
from accounts.models import User

import json

class SupportViewset(viewsets.ModelViewSet):
    serializer_class = SupportSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'add' or self.action == 'pop':
            return AddUserSerializer
        return SupportSerializer

    def update(self, request, pk):
        support = self.get_object()
        customers = Customer.objects.filter(support=pk)

        for customer in customers:

            data = json.loads(customer.data)
            extra_data = json.loads(customer.extra_data)

            for item in self.request.data['delFields']:
                # move from one list to another
                if data.get(item['name'],None):
                    extra_data[item['name']] = data[item['name']]
            for item in self.request.data['newFields']:
                # add field to the list
                data[item['name']] = ''

            customer.data = json.dumps(new_data)
            customer.extra_data = json.dumps(extra_data)
            customer.save()

        return super(SupportViewset, self).update(request, pk)

    def retrieve(self,request,pk=None):

        tickets = Ticket.objects.filter(support=pk)
        tickets = TicketSerializer(tickets,many=True)

        support = SupportSerializer(self.get_object())

        group = Group.objects.filter(name=support.data['name']+':'+str(support.data['id']))[0]
        users = User.objects.filter(groups=group.id)
        users = UserSerializer(users,many=True)

        return Response({'support': support.data,
                         'tickets': tickets.data,
                         'users': users.data
                         })

    def create(self, request, *args, **kwargs):
        super(SupportViewset, self).create(request, *args, **kwargs)
        return super(SupportViewset, self).list(request, *args, **kwargs)

    @detail_route(methods=['post','get'])
    def add(self, request, pk=None):
        if request.method == 'GET':
            support = get_object_or_404(Support, pk=pk)
            group = get_object_or_404(Group, name=support.name+':'+str(support.id))
            users = User.objects.exclude(groups=group)
            assigned = User.objects.filter(groups=group)
            users = UserSerializer(users,many=True)
            assigned = UserSerializer(assigned,many=True)
            return Response({"users": users.data,
                             "assigned":assigned.data})
        else:
            support = get_object_or_404(Support, pk=pk)
            group = get_object_or_404(Group, name=support.name+':'+str(support.id))
            user = get_object_or_404(User,pk=request.data['user_id'])
            group.user_set.add(user)
            users = User.objects.exclude(groups=group)
            assigned = User.objects.filter(groups=group)
            users = UserSerializer(users,many=True)
            assigned = UserSerializer(assigned,many=True)
            return Response({"users": users.data,
                             "assigned":assigned.data})

    @detail_route(methods=['post','get'])
    def pop(self, request, pk=None):
        if request.method == 'GET':
            support = get_object_or_404(Support, pk=pk)
            group = get_object_or_404(Group, name=support.name +':'+str(support.id))
            users = User.objects.exclude(groups=group)
            assigned = User.objects.filter(groups=group)
            users = UserSerializer(users,many=True)
            assigned = UserSerializer(assigned,many=True)
            return Response({"users": users.data,
                             "assigned":assigned.data})
        else:
            support = get_object_or_404(Support, pk=pk)
            group = get_object_or_404(Group, name=support.name+':'+str(support.id))
            user = get_object_or_404(User,pk=request.data['user_id'])
            group.user_set.remove(user)
            users = User.objects.exclude(groups=group)
            assigned = User.objects.filter(groups=group)
            users = UserSerializer(users,many=True)
            assigned = UserSerializer(assigned,many=True)
            return Response({"users": users.data,
                             "assigned":assigned.data})
