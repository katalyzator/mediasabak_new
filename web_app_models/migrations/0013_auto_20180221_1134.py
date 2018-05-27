# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-21 11:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0012_auto_20180221_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercisequestion',
            name='first_association',
            field=models.CharField(blank=True, help_text='"Это поле заполняется только в случае если вариантом вопроса вы выбрали "Сопоставление", оно будет отображаться как один из возможных ответов', max_length=255, null=True, verbose_name='Первый вариант ответа'),
        ),
        migrations.AddField(
            model_name='exercisequestion',
            name='second_association',
            field=models.CharField(blank=True, help_text='"Это поле заполняется только в случае если вариантом вопроса вы выбрали "Сопоставление", оно будет отображаться как один из возможных ответов', max_length=255, null=True, verbose_name='Второй вариант ответа'),
        ),
    ]