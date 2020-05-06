from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
from .models import Album, Song
  
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password','email']
        
class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['title', 'song_file']

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["username", "password"]

    def clean(self):
        if self.is_valid():
            if not authenticate(username=self.cleaned_data['username'], password=self.cleaned_data['password']):
                raise forms.ValidationError('Error, Invalid username or password!')