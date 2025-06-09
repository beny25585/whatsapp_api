from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Client, MessageQueue, FailedMessageAttempt, MessageSent, Contact
from unittest.mock import patch
from django.core.management import call_command

class SendMessageAPITest(APITestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(client_name="TestClient", api_key="12345")

    def test_send_message_success(self):
        url = reverse('send_message')
        data = {
            "client_name": "TestClient",
            "api_key": "12345",
            "phone": "0501234567",
            "name": "יוסי",
            "text": "שלום עולם"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 202)
        self.assertTrue(MessageQueue.objects.filter(contact__phone="0501234567").exists())

class ProcessQueueTest(APITestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(client_name="TestClient", api_key="12345")
        self.contact = Contact.objects.create(client=self.client_obj, name="יוסי", phone="0501234567")
        self.msg = MessageQueue.objects.create(client=self.client_obj, contact=self.contact, text="שלום", status="pending")

    @patch('whatsapp_app.process_queue.pywhatkit.sendwhatmsg_instantly')
    def test_process_queue_success(self, mock_send):
        mock_send.return_value = None
        call_command('process_queue')
        self.assertFalse(MessageQueue.objects.filter(id=self.msg.id).exists())
        self.assertTrue(MessageSent.objects.filter(phone="0501234567").exists())

    @patch('whatsapp_app.process_queue.pywhatkit.sendwhatmsg_instantly')
    def test_process_queue_failure(self, mock_send):
        mock_send.side_effect = Exception("Failed to send")
        call_command('process_queue')
        self.assertFalse(MessageQueue.objects.filter(id=self.msg.id).exists())
        self.assertTrue(FailedMessageAttempt.objects.filter(phone="0501234567").exists())
