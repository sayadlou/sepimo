# Generated by Django 3.2.13 on 2022-06-17 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0038_auto_20220617_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpage',
            name='title_en',
            field=models.CharField(default='Sepimo', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='blogpage',
            name='title_fa',
            field=models.CharField(default='Sepimo', max_length=60, null=True),
        ),
    ]