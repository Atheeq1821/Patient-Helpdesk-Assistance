from django.db import models

class Conversation(models.Model):
    user_input = models.TextField()
    model_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
