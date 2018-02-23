from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    type = models.IntegerField(default=0)
    email = models.EmailField(default='')
    registryTime = models.DateTimeField()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    createTime = models.DateTimeField()
