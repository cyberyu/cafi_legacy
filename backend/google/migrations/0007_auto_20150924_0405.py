# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0006_auto_20150918_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='string',
            field=models.CharField(max_length=1024),
        ),
    ]
