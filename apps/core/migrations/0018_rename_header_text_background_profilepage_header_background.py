# Generated by Django 3.2.13 on 2022-05-18 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20220518_1922'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profilepage',
            old_name='header_text_background',
            new_name='header_background',
        ),
    ]
