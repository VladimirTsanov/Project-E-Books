# Generated by Django 5.1.6 on 2025-04-26 15:28

import main.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_product_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='isbn',
            field=models.BigIntegerField(default=main.models.generate_isbn, unique=True),
        ),
    ]
