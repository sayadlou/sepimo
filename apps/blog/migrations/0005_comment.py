# Generated by Django 3.2.13 on 2022-06-18 13:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20220617_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('Published', 'Published'), ('Draft', 'Draft'), ('Trash', 'Trash')], max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('text', models.TextField(max_length=1000)),
                ('replay', models.TextField(max_length=1000)),
                ('pub_date', models.DateField(default=datetime.date.today, verbose_name='Date')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post')),
            ],
        ),
    ]