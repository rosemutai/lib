# Generated by Django 2.2.7 on 2020-02-12 14:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0027_auto_20200212_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 12, 17, 47, 36, 78642)),
        ),
    ]