# Generated by Django 2.2.7 on 2020-02-24 08:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0042_auto_20200217_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 11, 16, 57, 595783)),
        ),
    ]