# Generated by Django 5.0.6 on 2024-06-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Training", "0003_trainingmodule_total_pages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trainingmodule",
            name="file",
            field=models.FileField(
                blank=True, null=True, upload_to="Trainingcrm/media/uploads/"
            ),
        ),
    ]
