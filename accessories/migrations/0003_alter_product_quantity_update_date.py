# Generated by Django 4.1.5 on 2023-01-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0002_remove_product_remining_quantity_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='quantity_update_date',
            field=models.DateTimeField(),
        ),
    ]
