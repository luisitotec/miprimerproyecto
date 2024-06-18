# Generated by Django 4.2.11 on 2024-06-17 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0019_existencia_operador"),
    ]

    operations = [
        migrations.AddField(
            model_name="existencia",
            name="sucursal",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="tienda.sucursal",
            ),
        ),
    ]
