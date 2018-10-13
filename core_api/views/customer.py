from rest_framework import viewsets
from ..serializers.customer import CustomerSerializer
from ..serializers.chain import ChainSerializer
from ..models import Chain

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class CustomerViewset(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        super(CustomerViewset, self).create(request, *args, **kwargs)
        return super(CustomerViewset, self).list(request, *args, **kwargs)
