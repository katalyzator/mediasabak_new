# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-06 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0015_auto_20180304_0721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='file',
            new_name='book_file',
        ),
    ]