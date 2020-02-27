# Generated by Django 2.2.7 on 2019-11-21 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mpesa_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CheckoutRequestID', models.CharField(max_length=250, null=True)),
                ('ResultCode', models.IntegerField(null=True)),
                ('ResultDesc', models.CharField(max_length=250, null=True)),
                ('Amount', models.CharField(max_length=250, null=True)),
                ('MpesaReceiptNumber', models.CharField(max_length=250, null=True)),
                ('Balance', models.CharField(max_length=250, null=True)),
                ('TransactionDate', models.CharField(max_length=250, null=True)),
                ('PhoneNumber', models.CharField(max_length=250, null=True)),
            ],
            options={
                'ordering': ['TransactionDate'],
            },
        ),
        migrations.DeleteModel(
            name='MpesaCallBacks',
        ),
        migrations.DeleteModel(
            name='MpesaCalls',
        ),
        migrations.DeleteModel(
            name='MpesaPayment',
        ),
    ]
