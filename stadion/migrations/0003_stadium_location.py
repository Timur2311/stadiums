# Generated by Django 4.2.17 on 2025-03-14 04:34

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stadion", "0002_alter_stadium_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="stadium",
            name="location",
            field=django.contrib.gis.db.models.fields.PointField(
                blank=True, null=True, srid=4326
            ),
        ),
    ]
