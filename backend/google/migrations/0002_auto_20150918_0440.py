# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 18, 4, 40, 33, 400098), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchresult',
            name='doc_type',
            field=models.CharField(default='web', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='searchresult',
            name='text',
            field=models.TextField(default='', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='snippet',
            field=models.TextField(blank=True),
        ),
    ]
