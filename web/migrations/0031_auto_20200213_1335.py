# Generated by Django 2.2.7 on 2020-02-13 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0030_auto_20200213_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 13, 13, 35, 9, 715333)),
        ),
    ]