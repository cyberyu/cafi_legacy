# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('risk', '0006_remove_company_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='variations',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
    ]
