from django import forms
from django.contrib.auth.hashers import make_password, check_password

# Sign Up Form
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form

from userauth.models import User


class SignUpForm(ModelForm):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=254, help_text='Enter a password')
    phone_number = forms.CharField(max_length=32, required=False, help_text='Enter a valid phone number')
    email = forms.EmailField(max_length=32, required=False, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'phone_number',
            'password',
        ]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username exists!")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise ValidationError("Email exists!")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Phone_number exists!")
        return phone_number

    def clean_password(self):
        password = self.cleaned_data['password']
        return make_password(password)

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')
        if not email and not phone_number:
            raise ValidationError("You have to enter phone_number or email!")
        return cleaned_data


class LoginForm(Form):
    username = forms.CharField(max_length=32)
    password = forms.CharField(max_length=254, help_text='Enter a password')

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise ValidationError("Username does not exists!")
        return username

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        user = User.objects.get(username=cleaned_data['username'])
        if not check_password(cleaned_data['password'], user.password):
            raise ValidationError('Password is not correct!')
        return cleaned_data

    def retrieve_user(self):
        cleaned_data = self.clean()
        return User.objects.get(username=cleaned_data['username'])
