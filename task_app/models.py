from django.db import models
from django.contrib.auth.models import User

class Personality(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/')
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
    