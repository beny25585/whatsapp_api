from django.urls import path
from .views import SendWhatsAppMessage

urlpatterns = [
    path('send-message/', SendWhatsAppMessage.as_view(), name='send_message'),
]
