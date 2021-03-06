# Generated by Django 2.2.7 on 2020-02-27 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eLibrary', '0005_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.CharField(default='none', max_length=100)),
                ('rating', models.CharField(choices=[('0', '0'), ('.5', '.5'), ('1', '1'), ('1.5', '1.5'), ('2', '2'), ('2.5', '2.5'), ('3', '3'), ('3.5', '3.5'), ('4', '4'), ('4.5', '4.5'), ('5', '5')], default='2', max_length=3)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eLibrary.BookInstance')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eLibrary.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Borrower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(blank=True, null=True)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eLibrary.Book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eLibrary.Member')),
            ],
        ),
    ]
