# Generated by Django 5.0.6 on 2024-06-24 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Training", "0002_trainingmodule_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingmodule",
            name="total_pages",
            field=models.IntegerField(default=0),
        ),
    ]