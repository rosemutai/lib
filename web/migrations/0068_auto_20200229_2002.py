# Generated by Django 2.2 on 2020-02-29 17:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0067_auto_20200227_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='stationery',
            name='discount_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stationery',
            name='slug',
            field=models.SlugField(default=''),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 29, 20, 2, 20, 360252)),
        ),
    ]