# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0011_auto_20151011_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='geosearch',
            name='name',
            field=models.CharField(default='', max_length=100, blank=True),
            preserve_default=False,
        ),
    ]
