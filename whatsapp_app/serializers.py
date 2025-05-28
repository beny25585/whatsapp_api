from rest_framework import serializers
from .models import Client,Contact,Message

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields=['id','client_name','api_key']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields=['id','client','name', 'phone']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields=['id','client','contact','massege_type','text','status','timestapm','error_reason']  

class SendMessageSerializer(serializers.Serializer):
    api_key = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    message_type = serializers.CharField()
