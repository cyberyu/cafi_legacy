# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0005_company_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='project',
        ),
    ]
