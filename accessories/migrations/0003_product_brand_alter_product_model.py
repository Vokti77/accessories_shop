# Generated by Django 4.1.5 on 2023-06-06 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0002_remove_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accessories.brand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='model',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='accessories.model'),
        ),
    ]
