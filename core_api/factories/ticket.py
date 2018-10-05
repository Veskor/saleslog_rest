
import factory
import json

from .chain import ChainFactory, StatusFactory, ChatFactory
from .repair import RepairFactory
from .support import SupportFactory

from core_api.models import Ticket

import factory.fuzzy

class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    info = factory.fuzzy.FuzzyText()
    repair = factory.SubFactory(RepairFactory)
    support = factory.SubFactory(SupportFactory)
