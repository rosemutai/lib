# Generated by Django 2.2.7 on 2020-02-14 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0040_auto_20200213_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 14, 17, 55, 50, 830942)),
        ),
    ]