# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0009_auto_20160207_0339'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='locationalias',
            options={'verbose_name_plural': 'Location aliases'},
        ),
        migrations.AlterModelOptions(
            name='locationaliassecondaryname',
            options={'verbose_name': 'Secondary name'},
        ),
        migrations.AlterField(
            model_name='subdivision',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326),
        ),
    ]
