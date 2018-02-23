from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.TextField(max_length=100)
    date = models.DateField()


class GameInfo(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    content = models.TextField(max_length=255)
    orderid = models.IntegerField(default=-1)

