# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-08 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0011_auto_20161003_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]
