# Generated by Django 2.2.7 on 2020-02-27 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0065_auto_20200227_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 27, 17, 57, 59, 288074)),
        ),
    ]