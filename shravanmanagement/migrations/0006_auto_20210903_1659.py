# Generated by Django 3.0.7 on 2021-09-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shravanmanagement', '0005_user_profile_profilepic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_profile',
            name='profilepic',
            field=models.ImageField(blank=True, default='img/Photos-new-icon.png', null=True, upload_to='profile_pic/'),
        ),
    ]