from django.db import models

#שם האתר+מפתח יחודי
class Client(models.Model):
    client_name = models.CharField(max_length=100)
    api_key = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.client_name

#רשימה של אנשי קשר של הלקוח
class Contact(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.phone})"

#הודעה שנשלחה 
class Message(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=50)
    text = models.TextField()
    status = models.CharField(max_length=20)  # sent / failed
    timestamp = models.DateTimeField(auto_now_add=True)
    error_reason = models.TextField(null=True, blank=True)
