# Generated by Django 3.2.13 on 2022-06-13 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20220612_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='provence',
            field=models.CharField(default='', max_length=30, verbose_name='Provence'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.TextField(max_length=300, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=30, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=30, verbose_name='State'),
        ),
    ]