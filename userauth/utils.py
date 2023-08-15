import time

from django.contrib.auth import HASH_SESSION_KEY
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.authentication import BaseAuthentication

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


class Authentication(BaseAuthentication):
    def authenticate(self, request):
        session_hash = request.session.get(HASH_SESSION_KEY)
        if session_hash:
            try:
                payload = jwt_decode(session_hash)
                if payload["expires"] > time.time():
                    username = payload["username"]

                    try:
                        return User.objects.get(username=username), None
                    except User.DoesNotExist():
                        return None
            except:
                return None
        return None


def login_required(func):
    def new_func(cls, request, *args, **kwargs):
        user = get_user(request)
        if not user:
            return redirect(reverse_lazy('login'))
        request.user = user
        return func(cls, request, *args, **kwargs)

    return new_func
