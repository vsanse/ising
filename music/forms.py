from django import forms
from django.contrib.auth.models import User
#
from .models import Songs,Profile
#
#

#
#
class SongForm(forms.ModelForm):

    class Meta:
        model = Songs
        fields = ['artist','title','file']

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['name','dob','genre','photo','hometown']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']