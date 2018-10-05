import factory

import factory.fuzzy

from core_api.models import RepairNetwork, Repair, Part,\
                            Equipment, Engineer

class RepairNetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RepairNetwork

    name = "example network 1"

class PartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Part

    name = factory.fuzzy.FuzzyText(prefix='rx2_part_')
    quantity = factory.fuzzy.FuzzyInteger(1,42)
    network = factory.SubFactory(RepairNetworkFactory)

class EquipmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Equipment

    name = factory.fuzzy.FuzzyText(prefix='machine_')
    network = factory.SubFactory(RepairNetworkFactory)

class EngineerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Engineer

    username = factory.fuzzy.FuzzyText(prefix='user_')
    network = factory.SubFactory(RepairNetworkFactory)

class RepairFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repair

    network = factory.SubFactory(RepairNetworkFactory)
    part = factory.SubFactory(PartFactory)
    equipment = factory.SubFactory(EquipmentFactory)
    engineer = factory.SubFactory(EngineerFactory)
