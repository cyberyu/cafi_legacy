# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google', '0007_auto_20150930_0258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geosearchresult',
            name='search',
        ),
        migrations.DeleteModel(
            name='GeoSearchResult',
        ),
        migrations.RenameField(
            model_name='geosearch',
            old_name='string',
            new_name='address',
        ),
        migrations.AddField(
            model_name='geosearch',
            name='lat',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='geosearch',
            name='lng',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
