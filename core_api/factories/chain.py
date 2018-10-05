
import factory
import json

from core_api.models import Chain, Status, Chat, Message
import factory.fuzzy

from .customer import CustomerFactory

class ChainFactory(factory.Factory):
    class Meta:
        model = Chain

    customer = factory.SubFactory(CustomerFactory)

class StatusFactory(factory.Factory):
    class Meta:
        model = Status

    name = factory.fuzzy.FuzzyText(prefix='done_')
    color = factory.fuzzy.FuzzyText(length=5,prefix='#')
    chain = factory.SubFactory(ChainFactory)

class ChatFactory(factory.Factory):
    class Meta:
        model = Chat

    origin = factory.fuzzy.FuzzyChoice(choices=Chat.TYPE_CHOICES)
    tag = factory.SubFactory(ChainFactory)

class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    text = factory.fuzzy.FuzzyText()
    source = factory.fuzzy.FuzzyText()
    chat = factory.SubFactory(ChatFactory)
