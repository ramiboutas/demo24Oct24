# Generated by Django 5.1.2 on 2024-10-24 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="whatsapp_number",
            field=models.CharField(default="", max_length=16),
        ),
    ]