from django.db import models
from userauth.models import User


# Create your models here.

class Channel(models.Model):
    name = models.CharField(max_length=64)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Media(models.Model):
    size = models.IntegerField(max_length=10)
    format = models.CharField(max_length=60)
    type = models.CharField(max_length=60)
    duration = models.IntegerField(max_length=30, null=True)


class Post(models.Model):
    price = models.IntegerField(max_length=30, null=True)
    title = models.CharField(max_length=200, null=True)
    summary = models.CharField(max_length=400, null=True)
    content = models.CharField(max_length=1000)
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True)
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    is_vip = models.BooleanField(default=False)
