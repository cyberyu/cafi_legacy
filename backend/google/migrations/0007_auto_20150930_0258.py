# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('engagement', '0001_initial'),
        ('google', '0006_auto_20150918_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('string', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(related_name=b'geosearches', to='engagement.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeoSearchResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.CharField(max_length=255)),
                ('lng', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('search', models.ForeignKey(related_name=b'georesults', to='google.GeoSearch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='search',
            name='string',
            field=models.CharField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='searchresult',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
