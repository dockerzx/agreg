# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2019-05-23 02:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_feed_favicon'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='favicon',
            field=models.URLField(blank=True, null=True),
        ),
    ]
