# Generated by Django 2.2.7 on 2020-02-13 10:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0032_auto_20200213_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 13, 13, 40, 11, 256984)),
        ),
    ]
