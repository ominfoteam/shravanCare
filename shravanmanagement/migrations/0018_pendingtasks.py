# Generated by Django 3.0.7 on 2021-11-02 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shravanmanagement', '0017_auto_20211028_1358'),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingTasks',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('remark', models.TextField(blank=True, null=True)),
                ('duedate', models.DateField(blank=True, null=True)),
                ('notifyadmin', models.IntegerField(default=1, null=True)),
                ('taskfile', models.FileField(blank=True, default='', null=True, upload_to='taskfile/')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_task_create', to=settings.AUTH_USER_MODEL)),
                ('taskid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taskforeignkey', to='shravanmanagement.Task')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_task_update', to=settings.AUTH_USER_MODEL)),
                ('visitid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='visitid', to='shravanmanagement.IcareVisitScheduling')),
            ],
        ),
    ]
