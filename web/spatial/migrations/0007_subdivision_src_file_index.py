# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spatial', '0006_subdivision'),
    ]

    operations = [
        migrations.AddField(
            model_name='subdivision',
            name='src_file_index',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
