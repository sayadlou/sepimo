# Generated by Django 3.2.14 on 2022-08-04 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0039_auto_20220804_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cart'),
        ),
    ]
