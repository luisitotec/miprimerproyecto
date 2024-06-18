# Generated by Django 4.2.11 on 2024-06-14 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tienda", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="venta",
            name="departamento",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="venta",
            name="giro",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="venta",
            name="municipio",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="venta",
            name="nit",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="venta",
            name="registro",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="venta",
            name="tipo_operacion",
            field=models.CharField(
                choices=[
                    ("FAC_CONSUMIDOR_FINAL", "Factura Consumidor Final"),
                    ("CREDITO_FISCAL", "Crédito Fiscal"),
                ],
                default="FAC_CONSUMIDOR_FINAL",
                max_length=50,
            ),
        ),
    ]
