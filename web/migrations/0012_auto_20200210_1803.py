# Generated by Django 2.2.7 on 2020-02-10 15:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20200210_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 10, 18, 3, 1, 175171)),
        ),
    ]
