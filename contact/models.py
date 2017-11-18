from django.db import models
import datetime

# Create your models here.

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=60)
    subject = models.CharField(max_length=60)
    message = models.CharField(max_length=60)
    day_added = models.DateTimeField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)

    def __str__(self):
        return self.email
