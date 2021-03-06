# Generated by Django 3.0.7 on 2021-08-31 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shravanmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='icare_id_proof',
            name='is_vaccination',
            field=models.CharField(choices=[('YES', 'YES'), ('NO', 'NO')], default='NO', max_length=50),
        ),
        migrations.AlterField(
            model_name='icare_id_proof',
            name='imgurl',
            field=models.ImageField(blank=True, default='img/Photos-new-icon.png', null=True, upload_to='icareproof/'),
        ),
    ]
