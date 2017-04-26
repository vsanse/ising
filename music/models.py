from django.contrib.auth.models import Permission, User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=250)
    hometown=models.CharField(max_length=500)
    photo = models.FileField()


    def __str__(self):
        return self.name


class Song(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    genre = models.CharField(max_length=100,default='')

    def __str__(self):
        return self.song_title
