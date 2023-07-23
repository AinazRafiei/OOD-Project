import time

from django.db import models

# Create your models here.
from userauth.crypto import jwt_encode


class User(models.Model):
    username = models.CharField(max_length=64, db_index=True)
    email = models.CharField(max_length=64, null=True, blank=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    password = models.CharField(max_length=256)
    last_login = models.DateTimeField(null=True)

    LOGIN_EXPIRATION = 90 * 24 * 60 * 60  # 90 days

    def get_session_auth_hash(self):
        payload = {"id": self.id, "username": self.username, "expires": int(time.time() + self.LOGIN_EXPIRATION)}
        return jwt_encode(payload)
