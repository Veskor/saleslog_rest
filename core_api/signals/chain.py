from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from functools import wraps
import json

from ..serializers.chain import ChainSerializer, ChatSerializer

from ..models import *

# Chain post_save/delete methods to ensure chain is 1-1 with cusotmer.
# ---
@receiver(post_save, sender=Customer, dispatch_uid='create_chain')
def create_chain(sender, instance, created, **kwargs):

    if created:
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

@receiver(pre_delete, sender=Customer, dispatch_uid='create_chain')
def delete_chain(sender, instance, **kwargs):

    chain = Chain.objects.get(customer=instance.id)

    # Warning !!! when deleting customer chat/messages will be left behind and maybe will cause junk in system.
    # uncomment if we should start deleting them.

    #chat = Chat.objects.filter(tag=chain.id)
    #messages = Message.objects.filter(chat=chat.id)
    #for item in messages:
    #    item.delete()
    #chat.delete

    deleted = chain.delete()

# ---
# Utils for chain
# ---

def skip_signal():
    def _skip_signal(signal_func):
        @wraps(signal_func)
        def _decorator(sender, instance, **kwargs):
            if hasattr(instance, 'skip_signal'):
                return None
            return signal_func(sender, instance, **kwargs)
        return _decorator
    return _skip_signal

def safely_check_for_chain(instance):
    try:
        chain = instance.tag
        return chain
    except:
        return False

def create_a_chat_for_ticket(ticket, tag=None):
    if tag:
        chat = Chat.objects.create(origin=Chat.TICKET,tag=tag)
    else:
        chat = Chat.objects.create(origin=Chat.TICKET)

    # Defusing the bomb
    ticket.skip_signal = True
    chat.skip_signal = True

    # bip bip bip
    chat.save()
    ticket.chat = chat
    ticket.save()

    return chat

# ---
# Chain tickets field tracker for ticket id's
# ---

@receiver(post_save, sender=Ticket, dispatch_uid='update_ticket_list')
@skip_signal()
def update_chain(sender, instance, **kwargs):
    chain = safely_check_for_chain(instance)
    if chain:
        tickets = json.loads(str(chain.tickets))

        # assign a chat to a ticket
        chat = create_a_chat_for_ticket(instance)

        if not instance.id in tickets:
            tickets.append(instance.id)

        if instance.status:
            statuses = json.loads(str(chain.statuses))
            if not instance.status in statuses:
                tickets.append(instance.status.id)

        data = {'tickets':tickets}

        serialized = ChainSerializer(chain,data=data,partial=True)

        serialized.is_valid()

        saved = serialized.save()
    else:
        chat = create_a_chat_for_ticket(instance)

# Chat updater
@receiver(post_save, sender=Chat, dispatch_uid='update_chat_list')
@skip_signal()
def update_chain_chat(sender, instance, **kwargs):
    chain = safely_check_for_chain(instance)
    if chain:

        chats = json.loads(chain.chats)

        if not instance.id in chats:
            chats.append(instance.id)

        data = {'chats':chats}

        serialized = ChainSerializer(chain,data=data,partial=True)

        serialized.is_valid()

        saved = serialized.save()
