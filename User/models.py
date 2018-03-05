from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.IntegerField(default=0)
    email = models.EmailField(default='')
    registryTime = models.DateTimeField()

