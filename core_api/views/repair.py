from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Part, Equipment, Engineer
from ..serializers.support import SupportSerializer
from ..serializers.repair import RepairNetworkSerializer, EngineerSerializer,\
                                PartSerializer, EquipmentSerializer

class RepairNetworkViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = RepairNetworkSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def retrieve(self,request,pk=None):
        try:
            parts = Part.objects.filter(network=pk)
            equipment = Equipment.objects.filter(network=pk)
            engineers = Engineer.objects.filter(network=pk)
        except Exception as e:
            print('error:',e)
            return Response({'error':'Invalid network id'})
        return Response({
            'engineers': EngineerSerializer(engineers,many=True).data,
            'parts': PartSerializer(parts,many=True).data,
            'equipment': EquipmentSerializer(equipment,many=True).data
        })

class SupportViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = SupportSerializer
    queryset = serializer_class.Meta.model.objects.all()
