from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, FormView

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
            return redirect(reverse_lazy('home'))
        else:
            return self.form_invalid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('home'))


class Home(View):
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        # user.channels.all()
        return render(request, 'html/home.html', {"username": "hamed"})
