from rest_framework import serializers
from ..models import Repair, Part, Equipment, Status,\
                     Engineer, RepairNetwork, Support

class RepairNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairNetwork
        fields = ('id','name')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name')

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = ('id','name','quantity','network')

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id','name','network')

class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = ('id','username','network')

class RepairSerializer(serializers.ModelSerializer):

    class Meta:
        model = Repair
        fields = ('id','network','part','equipment','engineer')

    def create(self, validated_data):
        validated_data['network'] = RepairNetwork.objects.get(id=int(self.context.get('kwargs')['id']))
        return Repair(**validated_data)
#    def validate(self, data):
    # TODO: if part, equipment and engineer is assigned
    # set status from pending to ready .
