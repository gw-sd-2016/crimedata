# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0004_auto_20151025_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='incident',
            name='import_source',
            field=models.CharField(max_length=3, choices=[('ADM', 'Admin UI'), ('ARM', 'GWPD ARMS'), ('CHI', 'Chicago OpenData'), ('ZZZ', 'Other')], default='ADM'),
        ),
    ]
