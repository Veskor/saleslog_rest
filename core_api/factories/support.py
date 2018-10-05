import factory
import json
import random

from core_api.models import Support
from .repair import RepairNetworkFactory
import factory.fuzzy

class SupportFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Support

    name = factory.fuzzy.FuzzyText(prefix='sup_')
    ip = '{}.{}.{}.{}'.format('12','23','34','12')
    network = factory.SubFactory(RepairNetworkFactory)
    fields = [{
            'type':'int',
            'max':'5',
            'name':'rating',
            'args': [{'more':'data'}],
            }]
