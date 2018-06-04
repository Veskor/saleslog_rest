from rest_framework import viewsets
from rest_framework.response import Response
from ..models import Part, Equipment, Engineer, RepairNetwork
from ..serializers.support import SupportSerializer
from ..serializers.repair import RepairNetworkSerializer, EngineerSerializer,\
                                PartSerializer, EquipmentSerializer

class RepairNetworkViewset(viewsets.ModelViewSet):
#    authentication_classes = (TokenAuthentication,)
#    permission_classes = (IsAuthenticated,)
    serializer_class = RepairNetworkSerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self,request):
        # queryset.filter() filter po useru
        response = []
        for network in RepairNetwork.objects.all():
            pk = network.id
            parts = Part.objects.filter(network=pk)
            equipment = Equipment.objects.filter(network=pk)
            engineers = Engineer.objects.filter(network=pk)
            response.append({
                'id': network.id,
                'name': network.name,
                'engineers': EngineerSerializer(engineers,many=True).data,
                'parts': PartSerializer(parts,many=True).data,
                'equipment': EquipmentSerializer(equipment,many=True).data
                })
        return Response(response)

    def create(self, request, *args, **kwargs):
        print(request.data)
        obj = RepairNetworkSerializer(data=request.data)

        obj.is_valid()
        obj = obj.save()

        pk = obj.id

        parts = Part.objects.filter(network=pk)
        equipment = Equipment.objects.filter(network=pk)
        engineers = Engineer.objects.filter(network=pk)
        response = {
            'id': obj.id,
            'name': obj.name,
            'engineers': EngineerSerializer(engineers,many=True).data,
            'parts': PartSerializer(parts,many=True).data,
            'equipment': EquipmentSerializer(equipment,many=True).data
            }

        return Response(response)
# ovo mogu da vide inzinjeri i customeri i komentarisu. kao i support koji
# i svi admini iz suppporta za ovaj ticker.

class RepairViewset(viewsets.ModelViewSet):
    serializer_class = SupportSerializer
    queryset = serializer_class.Meta.model.objects.all()
