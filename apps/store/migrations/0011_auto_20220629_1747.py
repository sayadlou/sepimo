# Generated by Django 3.2.13 on 2022-06-29 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20220627_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='description',
            new_name='intro',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description_en',
            new_name='intro_en',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='description_fa',
            new_name='intro_fa',
        ),
    ]
