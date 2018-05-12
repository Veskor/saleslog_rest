from rest_framework import viewsets
from ..serializers.customer import CustomerSerializer

class CustomerViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    queryset = serializer_class.Meta.model.objects.all()
