# Generated by Django 4.1.5 on 2023-05-30 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_alter_service_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('Completed', 'Completed')], default='pending', max_length=25),
        ),
    ]
