# Generated by Django 4.2 on 2024-06-04 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_coupon_coupon_percent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]