# Generated by Django 2.2.7 on 2020-02-25 09:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0053_auto_20200225_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 25, 12, 23, 44, 932280)),
        ),
    ]
