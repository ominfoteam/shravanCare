# Generated by Django 3.0.7 on 2021-10-25 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shravanmanagement', '0014_auto_20211024_1654'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicemanagement',
            name='countervalue',
            field=models.IntegerField(default=0),
        ),
    ]
