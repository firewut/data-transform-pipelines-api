# Generated by Django 2.1.2 on 2018-11-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0006_pipelineresultfile_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="pipelineresultfile",
            name="extension",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
