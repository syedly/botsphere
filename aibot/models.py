from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomizeBot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    personality = models.TextField()
    
    def __str__(self):
        return self.name
    
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bot = models.ForeignKey(CustomizeBot, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    
    def __str__(self):
        return self.message