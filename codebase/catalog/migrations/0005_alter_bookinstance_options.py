# Generated by Django 5.1.2 on 2024-10-24 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_bookinstance_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bookinstance",
            options={"base_manager_name": "prefetch_manager", "ordering": ["due_back"]},
        ),
    ]