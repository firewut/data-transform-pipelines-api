# Generated by Django 2.1.2 on 2018-11-09 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0004_pipelineresultfile_mimetype"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processor",
            name="id",
            field=models.SlugField(
                editable=False, max_length=666, primary_key=True, serialize=False
            ),
        ),
    ]
