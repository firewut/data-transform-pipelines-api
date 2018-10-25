# Generated by Django 2.1.2 on 2018-10-23 10:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PipelineResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ctime', models.DateTimeField(auto_now_add=True, null=True)),
                ('error', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('is_finished', models.BooleanField(blank=True, default=False)),
                ('pipeline', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='projects.Pipeline')),
            ],
        ),
    ]