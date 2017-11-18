# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 17:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification_channels', '0006_auto_20171012_0220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='generator',
        ),
        migrations.AddField(
            model_name='notification',
            name='generator',
            field=models.ManyToManyField(blank=True, null=True, related_name='activity_notifications', to=settings.AUTH_USER_MODEL),
        ),
    ]
