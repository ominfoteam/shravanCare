# Generated by Django 3.0.7 on 2021-09-08 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shravanmanagement', '0008_auto_20210906_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='is_due',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=10, null=True),
        ),
    ]
