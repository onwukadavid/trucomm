# Generated by Django 4.2 on 2024-06-08 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='home_address',
            field=models.TextField(blank=True, null=True, verbose_name='home address'),
        ),
    ]
