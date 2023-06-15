# Generated by Django 4.1.5 on 2023-06-11 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0003_product_brand_alter_product_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='productquantityhistory',
            name='new_selling_price',
            field=models.DecimalField(decimal_places=2, default=55, max_digits=10),
            preserve_default=False,
        ),
    ]
