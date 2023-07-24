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


class Home(View):
    def get_channel_data(self, channel):
        post = Post.objects.filter(channel_id=channel.id).order_by('-published_at').first()
        summary = None
        published_at = None
        if post:
            summary = post.represent_summary()[1][:16]
            published_at = post.published_at
        return channel.id, channel.name, summary, published_at

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if user is None:
            return redirect(reverse_lazy('login'))
        channels = list()
        user_channels = Channel.objects.filter(owner=user)
        user_followings = Channel.objects.filter(id__in=Membership.objects.filter(user=user).values_list("channel_id"))

        def compare_datatime(x, y):
            if y[3] is None:
                return True
            if x[3] is None:
                return False
            return x[3] > y[3]

        return render(request, 'html/h.html', {"username": user.username})
