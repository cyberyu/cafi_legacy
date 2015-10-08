# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement', '0001_initial'),
        ('risk', '0004_remove_company_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='project',
            field=models.ManyToManyField(to='engagement.Project'),
            preserve_default=True,
        ),
    ]
