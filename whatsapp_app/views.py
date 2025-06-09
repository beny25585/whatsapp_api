from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client, Contact, MessageQueue, FailedMessageAttempt
from .serializers import SendMessageSerializer


class SendWhatsAppMessage(APIView):
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        api_key = serializer.validated_data['api_key']
        client_name = serializer.validated_data['client_name']
        phone = serializer.validated_data['phone']
        name = serializer.validated_data['name']

        try:
            client = Client.objects.get(api_key=api_key, client_name=client_name)
        except Client.DoesNotExist:
            FailedMessageAttempt.objects.create(
                client_name=client_name,
                api_key=api_key,
                phone=phone,
                name=name,
                reason=f"Invalid API key: '{api_key}' or client name: '{client_name}'"
            )
            return Response({"message": "Request received"}, status=status.HTTP_202_ACCEPTED)

        contact = Contact.objects.get_or_create(
            client_name=client_name,
            phone=phone,
            defaults={"name": name}
        )

        text = "the message sent"

        # מוסיפים לתור ההודעות
        MessageQueue.objects.create(
            client=client,
            contact=contact,
            text=text,
            status='pending'
        )

        return Response({"message": "Message sent to queue"}, status=status.HTTP_202_ACCEPTED)
