# Generated by Django 4.2 on 2024-06-06 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_cart_applied_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='coupon_percent',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
