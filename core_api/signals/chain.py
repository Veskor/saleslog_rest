from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import json

from ..serializers.chain import ChainSerializer, ChatSerializer

from ..models import *

# Chain post_save/delete methods to ensure chain is 1-1 with cusotmer.
# ---
@receiver(post_save, sender=Customer, dispatch_uid='create_chain')
def create_chain(sender, instance, **kwargs):

    # Chain
    data = {'customer': instance.id, 'tickets':'[]','chats':'[]','statuses':'[]'}

    chain = ChainSerializer(data=data)
    chain.is_valid()
    saved = chain.save()
    # Chat

    data = {'origin':'Master','tag':saved.id}
    chat = ChatSerializer(data=data)
    chat.is_valid()

    chat.save()

@receiver(post_save, sender=Customer, dispatch_uid='create_chain')
def delete_chain(sender, instance, **kwargs):

    chain = Chain.objects.filter(customer=instance.id)[0]

    # Warning !!! when deleting customer chat/messages will be left behind and maybe will cause junk in system.
    # uncomment if we should start deleting them.

    #chat = Chat.objects.filter(tag=chain.id)
    #messages = Message.objects.filter(chat=chat.id)
    #for item in messages:
    #    item.delete()
    #chat.delete

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

# Chat updater
@receiver(post_save, sender=Chat, dispatch_uid='update_chat_list')
def update_chain(sender, instance, **kwargs):
    chain = instance.tag

    chats = json.loads(chain.chats)

    if not instance.id in chats:
        chats.append(instance.id)

    data = {'chats':chats}

    serialized = ChainSerializer(chain,data=data,partial=True)

    serialized.is_valid()

    saved = serialized.save()

@receiver(post_delete, sender=Chat, dispatch_uid='alter_chat_list')
def alter_chain(sender, instance, **kwargs):
    chain = instance.tag

    chats = json.loads(chain.chats)
    chats.remove(instance.id)
    data = {'chats':chats}

    serialized = ChainSerializer(chain,data=data,partial=True)

    serialized.is_valid()

    saved = serialized.save()
