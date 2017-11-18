# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-06 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0006_auto_20171102_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_url', models.TextField()),
                ('homepage_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Homepage')),
            ],
        ),
    ]