# Generated by Django 5.0.6 on 2024-06-29 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0015_product_featured_product_season_product_special'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='season',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]