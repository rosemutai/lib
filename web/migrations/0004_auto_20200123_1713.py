# Generated by Django 2.2.7 on 2020-01-23 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20200123_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 1, 23, 17, 13, 49, 362887)),
        ),
    ]
