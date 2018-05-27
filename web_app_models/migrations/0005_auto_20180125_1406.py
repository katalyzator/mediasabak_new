# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-25 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0004_auto_20180125_0812'),
    ]

    operations = [
        migrations.CreateModel(
            name='MediaProjectsSlider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Картинка для слайдера')),
                ('text', models.CharField(max_length=255, verbose_name='Текст на картике')),
            ],
            options={
                'verbose_name': 'Слайдер',
                'verbose_name_plural': 'Слайдер на странице медиапроектов',
            },
        ),
        migrations.RemoveField(
            model_name='testanswer',
            name='point',
        ),
    ]