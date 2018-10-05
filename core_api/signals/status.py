from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json

from ..serializers.chain import ChainSerializer

from ..models import *

@receiver(post_save, sender=Status, dispatch_uid='update_ticket_list')
def update_status_chain(sender, instance, **kwargs):
    try:
        chain = instance.chain
    except:
        chain = ''
    if chain != '':

        statuses = json.loads(chain.statuses)

        if not instance.id in statuses:
            statuses.append(instance.id)

        data = {'statuses':statuses}

        serialized = ChainSerializer(chain,data=data,partial=True)

        serialized.is_valid()

        saved = serialized.save()

@receiver(post_delete, sender=Status, dispatch_uid='alter_ticket_list')
def alter_status_chain(sender, instance, **kwargs):
    try:
        chain = instance.chain
    except:
        chain = ''
    if chain != '':
        statuses = json.loads(chain.statuses)
        statuses.remove(instance.id)
        data = {'statuses':statuses}

        serialized = ChainSerializer(chain,data=data,partial=True)

        serialized.is_valid()

        saved = serialized.save()
