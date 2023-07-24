from django.db import models
from userauth.models import User


# Create your models here.


class Membership(models.Model):
    class Role(models.Choices):
        Owner = 'owner'
        Admin = 'admin'
        Normal = 'normal'
        Vip = 'vip'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey('Channel', on_delete=models.CASCADE)
    role = models.CharField(choices=Role.choices, default=Role.Normal, max_length=10)


class Channel(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    members = models.ManyToManyField(User, through=Membership, related_name="followings")


class Media(models.Model):
    size = models.IntegerField()
    format = models.CharField(max_length=60)
    type = models.CharField(max_length=60)
    duration = models.IntegerField(null=True)


class Post(models.Model):
    price = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    summary = models.CharField(max_length=400, null=True, blank=True)
    content = models.CharField(max_length=1000)
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    is_vip = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def represent_full(self):
        return [self.title, self.content, False, self.published_at.strftime("%B %d, %Y | %H:%M")]

    def represent_summary(self):
        if self.is_vip:
            return [self.title, self.summary, True, self.published_at.strftime("%B %d, %Y | %H:%M")]
        return self.represent_full()
