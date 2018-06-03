# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-06-03 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0025_auto_20180530_1744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Ответ', 'verbose_name_plural': 'Рандом Ответы'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Вопрос', 'verbose_name_plural': 'Рандом вопросы'},
        ),
        migrations.AddField(
            model_name='question',
            name='is_false',
            field=models.TextField(default=1, verbose_name='Текст если неправильно'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='is_true',
            field=models.TextField(default=1, verbose_name='Текст при правильном ответе'),
            preserve_default=False,
        ),
    ]
