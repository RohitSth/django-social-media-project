# Generated by Django 5.0 on 2024-01-11 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('car', '0007_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
