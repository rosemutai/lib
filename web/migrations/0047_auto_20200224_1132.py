# Generated by Django 2.2.7 on 2020-02-24 08:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0046_auto_20200224_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 11, 32, 58, 323720)),
        ),
    ]
