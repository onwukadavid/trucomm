# Generated by Django 4.2 on 2024-04-23 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_category_unique_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
