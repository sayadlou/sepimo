# Generated by Django 3.2.13 on 2022-05-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_alter_aboutuspage_main_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profilepage',
            name='menu_address',
            field=models.CharField(default='آدرس', max_length=60),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_address_en',
            field=models.CharField(default='آدرس', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_address_fa',
            field=models.CharField(default='آدرس', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_dashboard',
            field=models.CharField(default='داشبورد', max_length=60),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_dashboard_en',
            field=models.CharField(default='داشبورد', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_dashboard_fa',
            field=models.CharField(default='داشبورد', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_logout',
            field=models.CharField(default='خروج از حساب کاربری', max_length=60),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_logout_en',
            field=models.CharField(default='خروج از حساب کاربری', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_logout_fa',
            field=models.CharField(default='خروج از حساب کاربری', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_orders',
            field=models.CharField(default='سفارشات', max_length=60),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_orders_en',
            field=models.CharField(default='سفارشات', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_orders_fa',
            field=models.CharField(default='سفارشات', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_profile',
            field=models.CharField(default='جزئیات حساب کاربری', max_length=60),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_profile_en',
            field=models.CharField(default='جزئیات حساب کاربری', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='profilepage',
            name='menu_profile_fa',
            field=models.CharField(default='جزئیات حساب کاربری', max_length=60, null=True),
        ),
    ]