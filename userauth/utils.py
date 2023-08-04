import time

from django.contrib.auth import HASH_SESSION_KEY

from userauth.crypto import jwt_decode
from userauth.models import User


def get_user_id(request):
    session_hash = request.session.get(HASH_SESSION_KEY)
    if session_hash:
        try:
            payload = jwt_decode(session_hash)
            if payload["expires"] > time.time():
                return payload["username"]
        except:
            pass
    return None


def get_user(request):
    username = get_user_id(request)
    if not username:
        return None
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist():
        return None
    return user
