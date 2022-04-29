# Generated by Django 3.2.13 on 2022-04-29 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('W', 'Pending'), ('T', 'Transferred'), ('F', 'Failed')], default='W', max_length=20)),
                ('status_change_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('W', 'Waiting'), ('T', 'Transferred'), ('P', 'Payed'), ('F', 'Failed')], default='W', max_length=20)),
                ('status_change_date', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('price', models.DecimalField(decimal_places=0, max_digits=12)),
                ('max_order_quantity', models.DecimalField(decimal_places=0, max_digits=12)),
                ('min_order_quantity', models.DecimalField(decimal_places=0, max_digits=12)),
                ('purchaser', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product Base Model',
                'verbose_name_plural': 'Product Base Models',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('expired_at', models.DateTimeField(blank=True, null=True, verbose_name='expired at')),
                ('due_at', models.DateTimeField(blank=True, null=True, verbose_name='due at')),
                ('fulfilled_at', models.DateTimeField(blank=True, null=True, verbose_name='fulfilled at')),
                ('amount', models.PositiveIntegerField(default=0, verbose_name='amount')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'initial'), (2, 'processing'), (3, 'confirmed')], default=2, verbose_name='status')),
                ('status_change_date', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order', verbose_name='order')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order', verbose_name='order item')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'Order item',
                'verbose_name_plural': 'Order items',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='quantity')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.cart', verbose_name='cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
            options={
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
                'ordering': ('id',),
            },
        ),
    ]
