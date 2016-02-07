# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0007_subdivision_src_file_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationAlias',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('primary_display_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='LocationAliasSecondaryName',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('display_name', models.CharField(max_length=255)),
                ('location_alias', models.ForeignKey(to='spatial.LocationAlias')),
            ],
        ),
        migrations.AlterField(
            model_name='subdivision',
            name='polygon',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
        ),
    ]
