# Generated by Django 4.2.11 on 2024-06-15 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0003_existencia_detalle_venta"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="existencia",
            name="detalle_venta",
        ),
        migrations.AddField(
            model_name="detalleventa",
            name="existencia",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="detalleventa_set",
                to="tienda.existencia",
            ),
        ),
    ]
