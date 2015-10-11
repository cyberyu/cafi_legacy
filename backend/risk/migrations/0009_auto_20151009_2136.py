# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0008_auto_20151009_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='variations',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
