# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-12 11:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_channels', '0009_activity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='Type',
            new_name='notif_type',
        ),
    ]
