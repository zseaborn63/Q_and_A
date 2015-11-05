# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Q_and_A', '0002_auto_20151105_1914'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answer',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='question',
            new_name='body',
        ),
    ]
