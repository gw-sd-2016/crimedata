# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0002_incident_narrative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='lat',
            field=models.DecimalField(null=True, blank=True, decimal_places=6, max_digits=10),
        ),
        migrations.AlterField(
            model_name='incident',
            name='lon',
            field=models.DecimalField(null=True, blank=True, decimal_places=6, max_digits=10),
        ),
    ]
