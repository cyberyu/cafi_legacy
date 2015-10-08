# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement', '0001_initial'),
        ('risk', '0002_auto_20151008_2157'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='project',
            field=models.ForeignKey(default=1, to='engagement.Project'),
            preserve_default=False,
        ),
    ]
