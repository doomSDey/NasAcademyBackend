from django.db import models

# Create your models here.

class Slots(models.Model):
    slots = models.CharField(max_length=200)
    car = models.CharField(max_length=200)

class RateCount(models.Model):
    ip = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    date_time = models.CharField(max_length=200)
