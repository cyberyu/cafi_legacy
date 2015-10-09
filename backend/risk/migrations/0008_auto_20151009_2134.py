# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0007_company_variations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='zipcode',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
