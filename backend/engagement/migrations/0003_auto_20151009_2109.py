# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement', '0002_project_companies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='companies',
            field=models.ManyToManyField(to=b'risk.Company', blank=True),
        ),
    ]
