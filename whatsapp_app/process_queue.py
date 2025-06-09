# app/management/commands/process_queue.py

from django.core.management.base import BaseCommand
from .models import MessageQueue
import pywhatkit
from django.utils import timezone

class Command(BaseCommand):
    help = 'Process WhatsApp message queue'

    def handle(self, *args, **kwargs):
        pending_messages = MessageQueue.objects.get(status='pending')[:10]

        for msg in pending_messages:
            try:
                pywhatkit.sendwhatmsg_instantly(msg.contact.phone, msg.text)
                msg.status = 'sent'
                msg.sent_at = timezone.now()
                msg.error_reason = None
            except Exception as e:
                msg.status = 'failed'
                msg.error_reason = str(e)
            msg.save()
            self.stdout.write(self.style.SUCCESS(f"Processed message to {msg.contact.phone} - {msg.status}"))
