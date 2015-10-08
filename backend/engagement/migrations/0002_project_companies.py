# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0006_remove_company_project'),
        ('engagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='companies',
            field=models.ManyToManyField(to='risk.Company'),
            preserve_default=True,
        ),
    ]
