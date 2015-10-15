# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrimeType',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('friendly_name', models.CharField(max_length=240)),
                ('severity', models.IntegerField(default=5)),
            ],
        ),
        migrations.CreateModel(
            name='Incident',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField()),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=10)),
                ('incident_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='spatial.CrimeType')),
            ],
        ),
    ]
