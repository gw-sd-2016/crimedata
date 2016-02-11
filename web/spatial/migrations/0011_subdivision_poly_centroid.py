# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.contrib.gis.geos import Point

class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0010_auto_20160211_0135'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdivision',
            name='poly_centroid',
            field=django.contrib.gis.db.models.fields.PointField(default=Point(0,0), srid=4326),
            preserve_default=True,
        ),
    ]
