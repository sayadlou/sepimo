# Generated by Django 3.2.13 on 2022-06-24 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20220624_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_inventory',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),
    ]
