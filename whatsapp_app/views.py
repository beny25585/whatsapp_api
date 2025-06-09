from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Contact, MessageQueue
from .serializers import SendMessageSerializer
from django.core.exceptions import ObjectDoesNotExist
import pywhatkit


class SendWhatsAppMessage(APIView):
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        api_key = serializer.validated_data['api_key']
        phone = serializer.validated_data['phone']
        name = serializer.validated_data['name']
        message_type = serializer.validated_data['message_type']

        try:
            client = Client.objects.get(api_key=api_key)
        except Client.DoesNotExist:
            return Response({"error": "API key is missing or incorrect"}, status=status.HTTP_401_UNAUTHORIZED)

        contact, created = Contact.objects.get_or_create(
            client=client,
            phone=phone,
            defaults={"name": name}
        )

        text = "the message sent"

        MessageQueue.objects.create(
            client=client,
            contact=contact,
            text=text,
            status='pending'
        )

        return Response({"message": "message sent to que"}, status=status.HTTP_202_ACCEPTED)
