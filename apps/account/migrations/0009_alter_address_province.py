# Generated by Django 3.2.13 on 2022-06-17 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220613_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='province',
            field=models.CharField(max_length=30, verbose_name='Province'),
        ),
    ]
