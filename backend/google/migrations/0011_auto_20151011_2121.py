# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0010_auto_20151011_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geosearch',
            name='lat',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='geosearch',
            name='lng',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
