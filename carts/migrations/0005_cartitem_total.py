# Generated by Django 4.2 on 2024-06-03 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_remove_cartitem_updated_at_cartitem_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='total',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
