from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label = "이메일")
    hname = forms.CharField(label = "hname")
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")

class LoginForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("email", "password")

class SerialForm(forms.Form):
    serialcode = forms.CharField(label="serialcode")
    class Meta:
        fields = {"serialcode"}


class otpForm(forms.Form):
    otp = forms.CharField(label = 'otp')
    class Meta:
        fields = {"otp"}