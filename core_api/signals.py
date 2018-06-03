from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json

from .serializers.chain import ChainSerializer

from .models import *

# Chain post_save/delete methods to ensure chain is 1-1 with cusotmer.
# ---
@receiver(post_save, sender=Customer, dispatch_uid='create_chain')
def create_chain(sender, instance, **kwargs):
    data = {'customer': instance.id, 'tickets':[]}

    chain = ChainSerializer(data=data)
    chain.is_valid()

    saved = chain.save()

@receiver(post_save, sender=Customer, dispatch_uid='create_chain')
def create_chain(sender, instance, **kwargs):

    chain = Chain.objects.filter(customer=instance.id)[0]

    deleted = chain.delete()
# ---
# Chain tickets field tracker for ticket id's
# ---
@receiver(post_save, sender=Ticket, dispatch_uid='update_ticket_list')
def update_chain(sender, instance, **kwargs):
    chain = instance.tag

    tickets = json.loads(chain.tickets)

    if not instance.id in tickets:
        tickets.append(instance.id)

    data = {'tickets':tickets}

    serialized = ChainSerializer(chain,data=data,partial=True)

    serialized.is_valid()

    saved = serialized.save()

@receiver(post_delete, sender=Ticket, dispatch_uid='alter_ticket_list')
def alter_chain(sender, instance, **kwargs):
    chain = instance.tag

    tickets = json.loads(chain.tickets)
    tickets.remove(instance.id)
    data = {'tickets':tickets}

    serialized = ChainSerializer(chain,data=data,partial=True)

    serialized.is_valid()

    saved = serialized.save()
# ---
# Status
# ---
@receiver(post_save, sender=Status, dispatch_uid='update_ticket_list')
def update_status_chain(sender, instance, **kwargs):
    chain = instance.tag

    statuses = json.loads(chain.statuses)

    if not instance.id in statuses:
        statuses.append(instance.id)

    data = {'statuses':statuses}

    serialized = ChainSerializer(chain,data=data,partial=True)

    serialized.is_valid()

    saved = serialized.save()

@receiver(post_delete, sender=Status, dispatch_uid='alter_ticket_list')
def alter_status_chain(sender, instance, **kwargs):
    chain = instance.tag

    statuses = json.loads(chain.statuses)
    statuses.remove(instance.id)
    data = {'statuses':statuses}

    serialized = ChainSerializer(chain,data=data,partial=True)

    serialized.is_valid()

    saved = serialized.save()
# ---
