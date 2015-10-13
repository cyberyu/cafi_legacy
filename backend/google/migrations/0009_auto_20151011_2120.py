# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0008_auto_20151011_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geosearch',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='geosearch',
            name='lng',
        ),
    ]
