# Generated by Django 2.2 on 2020-03-05 14:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20200305_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 5, 17, 27, 50, 71340)),
        ),
    ]