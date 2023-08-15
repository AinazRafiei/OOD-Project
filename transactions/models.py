from django.db import models
from userauth.models import User


# Create your models here.


class TransactionCatalogue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=[('charge', 'شارژ'), ('withdraw', 'برداشت')])
    date = models.DateTimeField(auto_now_add=True)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0)
