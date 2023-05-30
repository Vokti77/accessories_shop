# Generated by Django 4.1.5 on 2023-05-29 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0011_alter_product_actual_sale_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='actual_Sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='buying_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='remining_quantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='sale_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
