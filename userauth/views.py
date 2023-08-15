from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView
from rest_framework.response import Response
from rest_framework.views import APIView

from channel.models import Channel, Membership, Post
from userauth.forms import SignUpForm, LoginForm
from userauth.utils import get_user


class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'html/signup.html'


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'html/login.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.retrieve_user()
            login(request, user)
            return redirect(reverse_lazy('channels'))
        else:
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('channels'))


class JoinView(APIView):
    def post(self, request, channel_id, *args, **kwargs):
        user = get_user(request)
        if user and not Membership.objects.filter(channel_id=channel_id, user_id=user.id).exists():
            Membership.objects.create(channel_id=channel_id, user_id=user.id)
        return Response()


class NavbarView(APIView):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        navbar = list()
        navbar.append(("/channels/", "Home"))
        if user:
            navbar.append(("/create_channel/", "Create Channel"))
            navbar.append(("/wallet/", "Wallet"))
            navbar.append(("/logout/", "Logout"))
        else:
            navbar.append(("/login/", "Login"))
            navbar.append(("/signup/", "Sign Up"))
        return Response(data=dict(navbar=navbar))
