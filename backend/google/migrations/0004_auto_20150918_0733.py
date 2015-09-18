# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0003_auto_20150918_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchresult',
            name='doc_type',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='search',
            field=models.ForeignKey(related_name=b'results', to='google.Search'),
        ),
    ]
