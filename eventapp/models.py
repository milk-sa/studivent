from django.db import models

# Create your models here.

class event(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField()
  date = models.DateTimeField()
  location = models.CharField(max_length=100)

