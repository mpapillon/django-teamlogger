# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-20 17:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nouvelles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=90),
        ),
    ]