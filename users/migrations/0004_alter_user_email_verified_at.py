# Generated by Django 4.2 on 2024-05-07 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email_verified_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]