# Generated by Django 3.2.14 on 2022-07-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_brand_brandpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='brandpage',
            name='title',
            field=models.CharField(default='Sepimo', max_length=60),
        ),
    ]