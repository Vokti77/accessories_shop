# Generated by Django 4.1.5 on 2023-05-29 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0010_alter_product_actual_sale_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='actual_Sale_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
