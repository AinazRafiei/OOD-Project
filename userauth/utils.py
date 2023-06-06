import time

from django.contrib.auth import HASH_SESSION_KEY

from userauth.crypto import jwt_decode


def get_username(request):
    session_hash = request.session.get(HASH_SESSION_KEY)
    if session_hash:
        try:
            payload = jwt_decode(session_hash)
            if payload["expires"] > time.time():
                return payload["username"]
        except:
            pass
    return None
