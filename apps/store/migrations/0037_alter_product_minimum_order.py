# Generated by Django 3.2.14 on 2022-08-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0036_auto_20220804_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='minimum_order',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
