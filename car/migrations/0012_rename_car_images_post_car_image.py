# Generated by Django 5.0 on 2024-01-20 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0011_alter_post_car_images'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='car_images',
            new_name='car_image',
        ),
    ]
