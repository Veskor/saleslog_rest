from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json

from .serializers.chain import ChainSerializer

from .models import *

@receiver(post_save, sender=Customer, dispatch_uid='create_chain')
def create_chain(sender, instance, **kwargs):
    data = {'customer': instance.id, 'tickets':[]}

    chain = ChainSerializer(data=data)
    chain.is_valid()

    saved = chain.save()

@receiver(post_save, sender=Ticket, dispatch_uid='update_ticket_list')
def update_chain(sender, instance, **kwargs):
    chain = instance.tag

    tickets = json.loads(chain.tickets)
    tickets.append(instance.id)
    data = {'tickets':tickets}

    serialized = ChainSerializer(chain,data=data,partial=True)
    try:
        serialized.is_valid()
    except Exception as e:
        print(e)

    saved = serialized.save()

@receiver(post_delete, sender=Ticket, dispatch_uid='alter_ticket_list')
def alter_chain(sender, instance, **kwargs):
    chain = instance.tag

    tickets = json.loads(chain.tickets)
    tickets.remove(instance.id)
    data = {'tickets':tickets}

    serialized = ChainSerializer(chain,data=data,partial=True)
    try:
        serialized.is_valid()
    except Exception as e:
        print(e)

    saved = serialized.save()
