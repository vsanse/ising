from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.

class Songs(models.Model):
    artist=models.CharField(max_length=100)
    title=models.CharField(max_length=250)
    file=models.FileField(default='')
    date=models.DateTimeField(auto_now_add=True)