# Generated by Django 5.1.2 on 2024-10-23 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("articles", "0003_article_featured"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "base_manager_name": "prefetch_manager",
                "ordering": ["-created_on"],
            },
        ),
    ]
