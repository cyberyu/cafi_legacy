# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0009_auto_20151011_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='geosearch',
            name='lat',
            field=models.FloatField(default=0, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geosearch',
            name='lng',
            field=models.FloatField(default=0, blank=True),
            preserve_default=False,
        ),
    ]
