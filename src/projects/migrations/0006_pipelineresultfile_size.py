# Generated by Django 2.1.2 on 2018-11-19 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20181109_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='pipelineresultfile',
            name='size',
            field=models.BigIntegerField(default=0),
        ),
    ]