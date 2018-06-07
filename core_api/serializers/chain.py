from ..models import Chain, Status, Chat, Message
from rest_framework import serializers

class ChainSerializer(serializers.ModelSerializer):

    tickets = serializers.JSONField()
    statuses = serializers.JSONField()
    chats = serializers.JSONField()

    class Meta:
        model = Chain
        fields = ('id','tickets','statuses','chats','customer')

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name','color')

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id','date','source','text','chat')

class ChatSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id','tag','messages','origin')

    def get_messages(self, obj):
        messages = Message.objects.filter(chat=obj.id)
        messages = MessageSerializer(messages,many=True)
        return messages.data
