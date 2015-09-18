# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0004_auto_20150918_0733'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='rank',
            field=models.IntegerField(default=1, blank=True),
            preserve_default=False,
        ),
    ]
