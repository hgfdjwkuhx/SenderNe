# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-11-03 21:34
from __future__ import unicode_literals

import SenderNeClientAPI.Commons.RandomIds
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SenderNeClientAPI', '0003_processorinfo_tempuserprivateprocessorinfo_userprivateprocessorinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tempuserprivateprocessorinfo',
            name='temp_token',
            field=models.TextField(default=SenderNeClientAPI.Commons.RandomIds.get_random_PrivateTempUser_TempUserToken),
        ),
    ]
