import factory
import json
import random

from core_api.models import Customer, Support, RepairNetwork

from .support import SupportFactory


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    data = "{}"
    support = SupportFactory()
    payment_done = True
