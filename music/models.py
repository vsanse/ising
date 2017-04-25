from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
from django.contrib.auth.models import Permission, User
class Profile(models.Model):
    user=models.ForeignKey(User,default=1)
    name=models.CharField(max_length=100)
    dob=models.DateField()
    genre=models.CharField(max_length=100)
    photo=models.ImageField()
    hometown=models.CharField(max_length=200)
class Songs(models.Model):
    user = models.ForeignKey(User, default=1)
    artist=models.ForeignKey(Profile)
    title=models.CharField(max_length=250)
    file=models.FileField(default='')
    date=models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField()
    is_liked=models.BooleanField(default=False)
