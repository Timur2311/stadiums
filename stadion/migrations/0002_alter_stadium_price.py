# Generated by Django 5.1.7 on 2025-03-13 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stadion", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stadium",
            name="price",
            field=models.DecimalField(
                decimal_places=2, max_digits=12, verbose_name="Price"
            ),
        ),
    ]
