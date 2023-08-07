from django.db import models

from userauth.models import User


# Create your models here.


class Membership(models.Model):
    class Role(models.TextChoices):
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


class Tariff(models.Model):
    class DurationChoice(models.IntegerChoices):
        Month = (30, 'Month')
        ThreeMonths = (90, 'Three Months')
        SixMonths = (180, 'Six Months')
        Year = (365, 'One Year')

    duration = models.IntegerField(choices=DurationChoice.choices)
    price = models.IntegerField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_duration_display()} = {self.price}$"


class Subscription(models.Model):
    user = models.ForeignKey(Membership, on_delete=models.CASCADE)
    until_date = models.DateTimeField()


class Share(models.Model):
    amount = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)


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
