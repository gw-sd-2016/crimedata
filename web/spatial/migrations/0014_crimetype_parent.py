# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0013_auto_20160211_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='crimetype',
            name='parent',
            field=models.ForeignKey(null=True, blank=True, related_name='child', to='spatial.CrimeType'),
        ),
    ]
