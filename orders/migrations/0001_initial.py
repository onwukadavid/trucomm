# Generated by Django 4.2 on 2024-06-12 22:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0014_alter_category_parent_category_and_more'),
        ('carts', '0011_cart_coupon_percent'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=25, unique=True)),
                ('quantity', models.PositiveBigIntegerField(blank=True, default=0, null=True)),
                ('amount', models.FloatField(blank=True, default=0, max_length=10, null=True)),
                ('status', models.CharField(blank=True, choices=[('Order Placed', 'Order Placed'), ('Order Confirmed', 'Order Confirmed'), ('Payment Processed', 'Payment Processed'), ('Order Processed', 'Order Processed'), ('Out for Delivery', 'Out for Delivery'), ('Delivered', 'Delivered'), ('Returned to Sender', 'Returned to Sender'), ('Cancelled', 'Cancelled'), ('Refunded', 'Refunded'), ('On Hold', 'On Hold')], default=None, max_length=255, null=True)),
                ('cart', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='carts.cart')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to='products.product')),
            ],
        ),
    ]
