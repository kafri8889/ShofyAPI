# Generated by Django 5.0.4 on 2024-04-16 14:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shofy_api', '0003_alter_product_quantity_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shofy_api.product'),
        ),
    ]