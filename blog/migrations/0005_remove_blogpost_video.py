# Generated by Django 5.1.6 on 2025-03-15 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_category_delete_blogcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='video',
        ),
    ]
