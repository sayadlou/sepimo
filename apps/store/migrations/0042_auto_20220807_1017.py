# Generated by Django 3.2.14 on 2022-08-07 10:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_userprofile_email'),
        ('store', '0041_auto_20220806_2238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('shipping_title', models.CharField(max_length=100)),
                ('shipping_coast', models.PositiveIntegerField(default=10000)),
                ('delivery_time', models.PositiveIntegerField(default=2)),
                ('minimum_order_cost', models.PositiveIntegerField(default=10000)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='account.address'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='discount',
            name='discount_purchase_amount',
            field=models.PositiveIntegerField(default=10000),
        ),
        migrations.AlterField(
            model_name='discount',
            name='minimum_purchase_amount',
            field=models.PositiveIntegerField(default=100000),
        ),
    ]
