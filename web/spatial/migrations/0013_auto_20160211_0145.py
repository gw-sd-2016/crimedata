# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.gis.geos import Point
from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0012_auto_20160211_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subdivision',
            name='poly_centroid',
            field=django.contrib.gis.db.models.fields.PointField(default=Point(0,0), srid=4326),
            preserve_default=False,
        ),
    ]
