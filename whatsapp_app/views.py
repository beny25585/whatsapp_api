from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client,Contact,Message
from .serializers import SendMessageSerializer
from django.shortcuts import get_object_or_404
import datetime
import pywhatkit

class SendWhatsAppMessage(APIView):
    def post(self, request):
        serializer = SendMessageSerializer(data=request.data)
        if serializer.is_valid():
            api_key = serializer.validated_data['api_key']
            phone = serializer.validated_data['phone']
            name = serializer.validated_data['name']
            message_type = serializer.validated_data['message_type']

            client = Client.objects.filter(api_key=api_key).first()
            if not client:
                return Response({"error": "API key לא תקין או חסר"}, status=status.HTTP_401_UNAUTHORIZED)

            contact, created = Contact.objects.get_or_create(
                client=client,
                phone=phone,
                defaults={"name": name}
            )

            message_type = "submission_success"
            text = "הפרטים נשלחו בהצלחה"

            sent_successfully = True

            message = Message.objects.create(
                client=client,
                contact=contact,
                message_type=message_type,
                text=text,
                status='sent' if sent_successfully else 'failed',
                error_reason=None if sent_successfully else 'שגיאה בשליחה'
            )

            try:
                pywhatkit.sendwhatmsg_instantly(phone, text,)
            except Exception as e:
                message.status = 'failed'
                message.error_reason = str(e)
                message.save()
                return Response({"error": f"שגיאה בשליחת ההודעה: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"success": True, "message": "הודעה נשלחה בהצלחה"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

