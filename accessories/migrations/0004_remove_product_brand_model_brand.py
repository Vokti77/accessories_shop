# Generated by Django 4.1.5 on 2023-05-09 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accessories", "0003_model_alter_product_model"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="brand",
        ),
        migrations.AddField(
            model_name="model",
            name="brand",
            field=models.ForeignKey(
                blank=True,
                default=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accessories.brand",
            ),
        ),
    ]