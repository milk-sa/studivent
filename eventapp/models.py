from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class event(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  date = models.DateField()
  location = models.CharField(max_length=100)

class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(event, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('yes', 'Yes'), ('no', 'No')])
    timestamp = models.DateTimeField(auto_now_add=True)