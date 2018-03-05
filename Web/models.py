from django.db import models
from User.models import User
from Admin.models import Administrator
# Create your models here.


class Visitor(models.Model):
    ip = models.TextField(max_length=15)
    user_agent = models.TextField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, default=None, null=True)
    visitTime = models.DateTimeField()


class Notice(models.Model):
    admin = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    title = models.TextField(max_length=50)
    content = models.TextField(max_length=255)
    createTime = models.DateTimeField()


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    createTime = models.DateTimeField()
