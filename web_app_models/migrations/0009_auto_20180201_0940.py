# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-01 09:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0008_auto_20180130_0523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Languages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(max_length=255, null=True, verbose_name='Язык')),
            ],
        ),
        migrations.AlterField(
            model_name='testquestion',
            name='type',
            field=models.CharField(choices=[('default', 'Стандартный'), ('video', 'Видео'), ('input', 'Текстовый'), ('image', 'Тест с картинками'), ('juxtaposition', 'Сопоставление'), ('multiple', 'Несколько вариантов ответа')], max_length=255, null=True, verbose_name='Тип вопроса'),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web_app_models.Languages', verbose_name='Язык книги'),
        ),
    ]