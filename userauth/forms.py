import re

from django import forms
from django.contrib.auth.hashers import make_password, check_password
# Sign Up Form
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form

from userauth.models import User

email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
phone_regex = re.compile(r'\+?[0-9]*')


class SignUpForm(ModelForm):
    username = forms.CharField(max_length=32, label="Nickname")
    identifier = forms.CharField(max_length=32, label="Email or Phone number")
    password = forms.CharField(max_length=254, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'password',
        ]
        widgets = {
            'email': forms.HiddenInput,
            'phone_number': forms.HiddenInput,
        }

    field_order = ['username', 'identifier', 'password']

    def clean(self):
        identifier = self.cleaned_data['identifier']
        if re.fullmatch(email_regex, identifier):
            if User.objects.filter(email=identifier).exists():
                raise ValidationError("Email exists!")
            self.cleaned_data['email'] = identifier
        elif re.fullmatch(phone_regex, identifier):
            if User.objects.filter(phone_number=identifier).exists():
                raise ValidationError("Phone number exists!")
            self.cleaned_data['phone_number'] = identifier
        else:
            raise ValidationError("Email or Phone number is not valid!")
        return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data['password']
        return make_password(password)


class LoginForm(Form):
    identifier = forms.CharField(max_length=32, label="Email or Phone number")
    password = forms.CharField(max_length=254, widget=forms.PasswordInput())

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise ValidationError("Username does not exists!")
        return username

    def clean_identifier(self):
        identifier = self.cleaned_data['identifier']
        if re.fullmatch(email_regex, identifier):
            if not User.objects.filter(email=identifier).exists():
                raise ValidationError("Email does not exists!")
            self.cleaned_data['email'] = identifier
        elif re.fullmatch(phone_regex, identifier):
            if not User.objects.filter(phone_number=identifier).exists():
                raise ValidationError("Phone number does not exists!")
            self.cleaned_data['phone_number'] = identifier
        else:
            raise ValidationError("Email or Phone number is not valid!")
        return identifier

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if self.errors.get('identifier'):
            return cleaned_data
        identifier = cleaned_data['identifier']
        if re.fullmatch(email_regex, identifier):
            user = User.objects.get(email=identifier)
        else:
            user = User.objects.get(phone_number=identifier)
        if not check_password(cleaned_data['password'], user.password):
            raise ValidationError('Password is not correct!')
        return cleaned_data

    def retrieve_user(self):
        cleaned_data = self.clean()
        identifier = cleaned_data['identifier']
        if re.fullmatch(email_regex, identifier):
            user = User.objects.get(email=identifier)
        else:
            user = User.objects.get(phone_number=identifier)
        return user
