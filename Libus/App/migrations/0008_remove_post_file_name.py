# Generated by Django 5.1 on 2024-08-13 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_post_file_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='file_name',
        ),
    ]
