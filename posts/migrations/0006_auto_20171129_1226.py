# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-29 09:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20171129_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='photo_medium',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='post',
            name='photo_thumb',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]