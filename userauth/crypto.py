import jwt
from django.conf import settings


def jwt_encode(payload):
    return jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256', headers={"kid": "0"})


def jwt_decode(token):
    return jwt.decode(token, settings.JWT_SECRET, algorithms='HS256')
