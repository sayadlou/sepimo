# Generated by Django 3.2.13 on 2022-06-30 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_remove_product_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='has_variant',
        ),
    ]
