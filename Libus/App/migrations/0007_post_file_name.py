# Generated by Django 5.1 on 2024-08-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_rename_is_image_post_is_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_name',
            field=models.CharField(default='', max_length=50000),
        ),
    ]