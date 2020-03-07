# Generated by Django 2.2 on 2020-03-05 13:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stationery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('slug', models.SlugField(default='', unique=True)),
                ('item_img', models.ImageField(default='', upload_to='stationaries_images')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 5, 16, 32, 20, 128949)),
        ),
    ]