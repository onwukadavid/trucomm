# Generated by Django 4.2 on 2024-06-04 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_alter_cartitem_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('no_of_usage', models.PositiveIntegerField(default=0)),
                ('expires_at', models.DateTimeField()),
                ('is_expired', models.BooleanField(default=False)),
            ],
        ),
    ]