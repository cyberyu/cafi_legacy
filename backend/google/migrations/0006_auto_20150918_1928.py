# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0005_searchresult_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresult',
            name='rank',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
