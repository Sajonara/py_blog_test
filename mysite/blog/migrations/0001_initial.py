# Generated by Django 5.2.4 on 2025-07-08 18:50

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("content", models.TextField()),
                (
                    "published_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DF", "Draft"),
                            ("PB", "Published"),
                            ("AR", "Archived"),
                            ("DL", "Deleted"),
                        ],
                        default="DF",
                        max_length=2,
                    ),
                ),
            ],
            options={
                "ordering": ["-published_at"],
                "indexes": [
                    models.Index(
                        fields=["-published_at"], name="blog_post_publish_2c9212_idx"
                    )
                ],
            },
        ),
    ]
