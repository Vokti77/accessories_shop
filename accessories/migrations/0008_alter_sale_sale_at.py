# Generated by Django 4.1.5 on 2023-05-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessories', '0007_productquantityhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_at',
            field=models.DateField(),
        ),
    ]
