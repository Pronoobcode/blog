# Generated by Django 5.1.6 on 2025-03-08 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='images/profile.webp', null=True, upload_to=''),
        ),
    ]
