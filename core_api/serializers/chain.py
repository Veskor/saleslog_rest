from ..models import Chain, Status, Chat, Message, Relation, StatusType
from rest_framework import serializers

class ChainSerializer(serializers.ModelSerializer):

    tickets = serializers.JSONField()
    statuses = serializers.JSONField()
    chats = serializers.JSONField()

    class Meta:
        model = Chain
        fields = ('id','tickets','statuses','chats','customer')

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation
        fields = ('model','model_id','id','name')

    # def validate(self, data):
    #     for item in Relation.objects.all():
    #         name = data['model'] + ' ' + str(data['model_id'])
    #         if name == str(item):
    #             return False
    #     return data
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name','color','status_type')

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
