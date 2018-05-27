# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-21 11:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0011_auto_20180203_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercisequestion',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_question', to='web_app_models.Exercise', verbose_name='Упражнение'),
        ),
        migrations.AlterField(
            model_name='exercisequestion',
            name='type',
            field=models.CharField(choices=[('default', 'Стандартный'), ('video', 'Видео'), ('input', 'Текстовый'), ('image', 'Тест с картинками'), ('juxtaposition', 'Сопоставление'), ('multiple', 'Несколько вариантов ответа')], default='default', max_length=255, null=True, verbose_name='Тип вопроса'),
        ),
    ]
