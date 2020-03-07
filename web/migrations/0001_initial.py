# Generated by Django 2.2 on 2020-03-05 12:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Art',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('item_img', models.ImageField(default='', upload_to='')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_name', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('edition', models.CharField(max_length=25)),
                ('ISBN', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('description', models.CharField(default=' ', max_length=50)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('book_img', models.ImageField(default='', upload_to='')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='BookLists',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone', models.IntegerField(default='')),
                ('email', models.EmailField(default='', max_length=254)),
                ('list_img', models.ImageField(default='', upload_to='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('checkout_request_id', models.CharField(default='', max_length=250)),
                ('transaction_initiated', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('item_img', models.ImageField(default='', upload_to='')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GroupOfCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_id', models.IntegerField()),
                ('ISBN', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='GuestSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guest_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('F', 'Fiction'), ('SCI', 'Sciences'), ('ROM', 'Romantic'), ('MYST', 'Mysteries'), ('HIST', 'Historical'), ('DET', 'Detective')], max_length=10)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('slug', models.SlugField(default='', unique=True)),
                ('description', models.TextField(default='')),
                ('image', models.ImageField(upload_to='novels')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=20)),
                ('last_name', models.CharField(default='', max_length=20)),
                ('email', models.EmailField(default='', max_length=254)),
                ('location', models.CharField(default='', max_length=20)),
                ('phone', models.IntegerField(default='')),
                ('Description', models.TextField(blank=True, max_length=255)),
                ('payment_status', models.BooleanField(default=False)),
                ('discount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pen',
            fields=[
                ('serial_number', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=20)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('item_img', models.ImageField(default='', upload_to='')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('in_stock', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('item_img', models.ImageField(default='', upload_to='')),
                ('available', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ShopApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopName', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=250)),
                ('accept', models.BooleanField(default=False)),
                ('cancel', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.User')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Book')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, default='', max_length=50)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.GroupOfCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ISBN', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField(default=5)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 3, 5, 15, 59, 37, 324004))),
                ('quantity', models.IntegerField(default=0)),
                ('paid', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.User')),
            ],
        ),
        migrations.CreateModel(
            name='bookshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Book')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.ShopApplication')),
            ],
        ),
        migrations.CreateModel(
            name='BookListsItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(default=5)),
                ('quantity', models.IntegerField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Book')),
                ('booklist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.BookLists')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Category'),
        ),
    ]
