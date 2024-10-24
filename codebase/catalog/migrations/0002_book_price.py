# Generated by Django 5.1.2 on 2024-10-24 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="price",
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=5),
        ),
    ]
