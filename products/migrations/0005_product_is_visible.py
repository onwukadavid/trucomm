# Generated by Django 4.2 on 2024-04-25 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_alter_category_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_visible',
            field=models.BooleanField(default=False),
        ),
    ]
