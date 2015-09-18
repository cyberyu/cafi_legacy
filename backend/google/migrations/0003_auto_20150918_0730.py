# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0002_auto_20150918_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='project',
            field=models.ForeignKey(related_name=b'searches', to='engagement.Project'),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='search',
            field=models.ForeignKey(related_name=b'documents', to='google.Search'),
        ),
    ]
