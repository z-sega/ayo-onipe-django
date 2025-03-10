# Generated by Django 5.1.6 on 2025-03-07 02:43

import django.utils.timezone
import model_utils.fields
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
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255)),
                ("slug", models.SlugField(blank=True, unique=True)),
                ("org_content", models.TextField(help_text="Raw Org-mode content")),
                (
                    "html_content",
                    models.TextField(
                        editable=False, help_text="Generated HTML content from Org-mode"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
