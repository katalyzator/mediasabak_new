# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-20 10:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web_app_models', '0016_auto_20180306_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseanswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_answer', to='web_app_models.ExerciseQuestion', verbose_name='Ответ к'),
        ),
    ]