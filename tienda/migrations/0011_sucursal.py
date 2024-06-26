# Generated by Django 4.2.11 on 2024-06-17 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0010_proveedor"),
    ]

    operations = [
        migrations.CreateModel(
            name="Sucursal",
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
                ("nombre", models.CharField(max_length=100)),
                ("direccion", models.CharField(max_length=200)),
                ("ciudad", models.CharField(max_length=100)),
                ("telefono", models.CharField(max_length=20)),
                ("email", models.EmailField(blank=True, max_length=100, null=True)),
                ("encargado", models.CharField(blank=True, max_length=100, null=True)),
                ("bodega", models.CharField(max_length=100)),
            ],
        ),
    ]
