# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0008_auto_20160207_0338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationalias',
            name='polygon',
        ),
        migrations.AddField(
            model_name='locationalias',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(default=None, srid=4326),
            preserve_default=False,
        ),
    ]
