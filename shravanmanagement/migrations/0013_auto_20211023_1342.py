# Generated by Django 3.0.7 on 2021-10-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shravanmanagement', '0012_auto_20211021_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icarevisitscheduling',
            name='visitstatus',
            field=models.CharField(choices=[('Not Visited', 'Not Visited'), ('Visited', 'Visited'), ('Not Confirmed', 'Not Confirmed')], default='Not Confirmed', max_length=50, null=True),
        ),
    ]
