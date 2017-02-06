# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-06 14:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0030_auto_20170206_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsubmission',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='bulletin.Form'),
        ),
    ]