from rest_framework import viewsets
from rest_framework import filters

from ..serializers.customer import CustomerSerializer, StatusCustomerSerializer
from ..serializers.chain import ChainSerializer, StatusSerializer
from ..models import Chain, Status
from ..decorators import create_sub_model_on_detail
from ..pagination import LargeResultsSetPagination

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route

import json

class FilterJSON(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        if 'search' in request.GET:
            search = request.GET['search']
        else:
            return queryset

        filtered_queryset = list()

        for item in queryset:
            data = json.loads(item.data.replace('\'','\"'))
            for field in data:
                if search in data[field]:
                    filtered_queryset.append(item)

        return filtered_queryset

class CustomerViewset(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (FilterJSON,)

    def get_serializer_class(self):
        if self.action == 'status':
            return StatusCustomerSerializer
        else:
            return CustomerSerializer

    def create(self, request, *args, **kwargs):
        super(CustomerViewset, self).create(request, *args, **kwargs)
        return super(CustomerViewset, self).list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        try:
            pk = request.GET.get('pk','')
            self.queryset = self.queryset.filter(support=pk)
        except:
            pass

        return super(CustomerViewset, self).list(request, *args, **kwargs)

    @detail_route(methods=['put','get'])
    @create_sub_model_on_detail(StatusSerializer)
    def status(self, request, obj, pk=None):
        customer = self.get_object()
        if request.method == 'GET':
            return Response(customer.support.id)
        if obj:
            status = obj.instance
        else:
            status = Status.objects.get(id=request.data['id'])

        print(status)
        chain = Chain.objects.get(customer=customer.id)

        statuses = json.loads(chain.statuses)

        if status.status_type.relation.model == 'Support':
            if status.status_type.relation.model_id == customer.support.id:
                if status.id not in statuses:
                    statuses.append(status.id)
                    chain.statuses = json.dumps(statuses)
                    chain.save()
                    return Response('Status successfuly added to customer')
                else:
                    return Response('Status allready added')
        return Response('support ids not matching')
