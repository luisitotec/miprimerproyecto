# Generated by Django 4.2.11 on 2024-06-15 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0004_remove_existencia_detalle_venta_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="existencia",
            name="id_venta",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
