from rest_framework import serializers
from .models import Client,Contact,MessageQueue

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
        model = MessageQueue
        fields=['id','client_name','contact','text','status','timestamp','error_reason']  

class SendMessageSerializer(serializers.Serializer):
    client_name = serializers.CharField(max_length=100)
    api_key = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)

