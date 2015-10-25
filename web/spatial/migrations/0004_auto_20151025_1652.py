# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0003_auto_20151025_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='lat',
            field=models.DecimalField(max_digits=10, default=0, decimal_places=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incident',
            name='lon',
            field=models.DecimalField(max_digits=10, default=0, decimal_places=6),
            preserve_default=False,
        ),
    ]
