# Generated by Django 5.1.6 on 2025-03-12 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blogpost_image_blogpost_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='category',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='BlogCategory',
        ),
    ]
