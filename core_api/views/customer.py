from rest_framework import viewsets
from ..serializers.customer import CustomerSerializer
from ..serializers.chain import ChainSerializer
from ..models import Chain

from rest_framework.response import Response

class CustomerViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self,request):
        customers = []
        for item in self.queryset:
            data = CustomerSerializer(item)

            chain = Chain.objects.filter(customer=item.id)[0]
            data = data.data
            data.update({'chain':chain.id})
            customers.append(data)
        return Response(customers)
