# Generated by Django 2.2.7 on 2020-02-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eLibrary', '0006_borrower_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_id',
            field=models.CharField(max_length=12, primary_key=True, serialize=False),
        ),
    ]
