# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-28 17:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0016_song_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Profile')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Song')),
            ],
        ),
    ]