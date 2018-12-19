from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, api_view

import json

from ..decorators import create_sub_model_on_detail
from ..models import Chain, Status, Support
from ..pagination import LargeResultsSetPagination
from ..serializers.chain import ChainSerializer, StatusSerializer
from ..serializers.customer import CustomerSerializer,\
                                   StatusCustomerSerializer,\
                                   StatusCustomerDeleteSerializer,\
                                   FileUploadSerializer

def get_statuses(ids):
    statuses = []

    for id in ids:
        data = StatusSerializer(instance=Status.objects.get(id=id))
        statuses.append(data.data)
    return statuses

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

@api_view(['GET', 'POST'])
def upload_file(request):
    if request.method == 'GET':
        return Response(FileUploadSerializer().data)

    up_file = request.FILES['file']
    destination = open('/media/customer_files/' + up_file.name, 'wb+')

    for chunk in up_file.chunks():
        destination.write(chunk)

    destination.close()

    return Response(destination.name)

class CustomerViewset(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (FilterJSON,)

    def get_serializer_class(self):
        if self.action == 'status':
            if self.request.method == 'PUT':
                return StatusCustomerDeleteSerializer
            return StatusCustomerSerializer
        else:
            return CustomerSerializer

    def list(self, request, *args, **kwargs):
        try:
            pk = request.GET.get('pk','')
            self.queryset = self.queryset.filter(support=pk)
        except:
            pass

        if len(self.queryset) == 0:
            support = Support.objects.get(pk=pk)
            header = []
            try:
                for item in json.loads(support.fields):
                    header.append(item['name'])
            except:
                header = []

            return Response(header)
        return super(CustomerViewset, self).list(request, *args, **kwargs)

    @detail_route(methods=['put','get','post'])
    @create_sub_model_on_detail(StatusSerializer)
    def status(self, request, obj, pk=None):
        customer = self.get_object()
        chain = Chain.objects.get(customer=customer.id)
        statuses = json.loads(chain.statuses)

        if request.method == 'PUT':
            status = Status.objects.get(id=request.data['id'])

            if status.id in statuses:
                statuses.remove(status.id)
                chain.statuses = json.dumps(statuses)
                chain.save()
                return Response(get_statuses(statuses))

        if request.method == 'GET':
            return Response(get_statuses(statuses))

        if obj:
            status = obj.instance
        else:
            status = Status.objects.get(id=request.data['id'])

        if status.status_type.relation.model == 'Support':
            if status.status_type.relation.model_id == customer.support.id:
                if status.id not in statuses:
                    statuses.append(status.id)
                    chain.statuses = json.dumps(statuses)
                    chain.save()
                    return Response(get_statuses(statuses))
                else:
                    return Response('Status allready added')

        return Response('support ids not matching')
