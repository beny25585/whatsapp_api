from django.core.management.base import BaseCommand
from whatsapp_app.models import MessageQueue, FailedMessageAttempt, MessageSent
import pywhatkit
from django.utils import timezone

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        messages_to_process = MessageQueue.objects.filter(status='pending').order_by('created_at')[:10]

        for msg in messages_to_process:
            try:
                pywhatkit.sendwhatmsg_instantly(msg.contact.phone, msg.text)

                MessageSent.objects.create(
                    client_name=msg.client.client_name,
                    api_key=msg.client.api_key,
                    phone=msg.contact.phone,
                    name=msg.contact.name,
                    timestamp=timezone.now()
                )

                msg.delete()

                self.stdout.write(self.style.SUCCESS(f"Sent to {msg.contact.phone}"))

            except Exception as e:
                FailedMessageAttempt.objects.create(
                    client_name=msg.client.client_name,
                    api_key=msg.client.api_key,
                    phone=msg.contact.phone,
                    name=msg.contact.name,
                    timestamp=timezone.now(),
                    reason=str(e)
                )

                msg.delete()

                self.stdout.write(self.style.ERROR(f"Failed to send to {msg.contact.phone}: {str(e)}"))
