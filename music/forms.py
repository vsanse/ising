from django import forms
from django.contrib.auth.models import User

from .models import Profile, Song


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name', 'hometown','photo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file','genre']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
