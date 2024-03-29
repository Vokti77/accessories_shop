# Generated by Django 4.1.5 on 2023-06-06 11:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to='accessories.brand')),
            ],
        ),
        migrations.CreateModel(
            name='MonthlySaleProfitHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_quantity', models.PositiveIntegerField()),
                ('stock_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sale_quantity', models.PositiveBigIntegerField()),
                ('sale_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_quantity', models.PositiveIntegerField()),
                ('buying_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sale_quantity', models.PositiveIntegerField(default=0)),
                ('expecting_Saleing_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('actual_Sale_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('remining_quantity', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('added_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to='accessories.brand')),
                ('model', models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to='accessories.model')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sale_quantity', models.PositiveIntegerField(default=0)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_Sale_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('profit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('sale_at', models.DateField()),
                ('update_at', models.DateField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='accessories.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductQuantityHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_added', models.PositiveIntegerField()),
                ('buying_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('added_at', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accessories.product')),
            ],
        ),
    ]
