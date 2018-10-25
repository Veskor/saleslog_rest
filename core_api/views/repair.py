from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Part, Equipment, Engineer, RepairNetwork, Repair
from ..serializers.support import SupportSerializer
from ..serializers.repair import RepairNetworkSerializer, EngineerSerializer, StatusSerializer,\
                                PartSerializer, EquipmentSerializer, RepairSerializer

class RepairNetworkViewset(viewsets.ModelViewSet):
    serializer_class = RepairNetworkSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = None


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
        obj = RepairNetworkSerializer(data=request.data)

        if not obj.is_valid():
            res = Response(obj.errors)
            res.status_code = 400
            return res

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
    serializer_class = RepairSerializer
    queryset = serializer_class.Meta.model.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self, *args, **kwargs):
        return Repair.objects.filter(network=self.kwargs['id'])

    def create(self, request, *args, **kwargs):
        request.POST['network'] = self.kwargs['id']
        return super(RepairViewset, self).create(request, *args, **kwargs)
