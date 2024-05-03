# Generated by Django 4.2 on 2024-05-01 11:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 1, 12, 23, 56, 804948), verbose_name='created at'),
        ),
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
    ]