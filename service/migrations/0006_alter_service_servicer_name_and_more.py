# Generated by Django 4.1.5 on 2023-05-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0005_alter_service_servicer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='servicer_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='service',
            name='sevicing_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
