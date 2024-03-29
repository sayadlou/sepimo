# Generated by Django 3.2.13 on 2022-06-24 20:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
                ('title_fa', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('title_en', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('about_blog_active', models.BooleanField(default=False)),
                ('about_blog_title', models.CharField(blank=True, max_length=50, null=True)),
                ('about_blog_text', models.TextField(blank=True, max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactUsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactUsThanksPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='homePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrdersPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SignPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
                ('title_fa', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('title_en', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('background_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='signup_page', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfilePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
                ('title_fa', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('title_en', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('header_text_big', models.CharField(max_length=60)),
                ('header_text_big_fa', models.CharField(max_length=60, null=True)),
                ('header_text_big_en', models.CharField(max_length=60, null=True)),
                ('header_text_small', models.CharField(max_length=60)),
                ('header_text_small_fa', models.CharField(max_length=60, null=True)),
                ('header_text_small_en', models.CharField(max_length=60, null=True)),
                ('menu_dashboard', models.CharField(default='داشبورد', max_length=60)),
                ('menu_dashboard_fa', models.CharField(default='داشبورد', max_length=60, null=True)),
                ('menu_dashboard_en', models.CharField(default='داشبورد', max_length=60, null=True)),
                ('menu_orders', models.CharField(default='سفارشات', max_length=60)),
                ('menu_orders_fa', models.CharField(default='سفارشات', max_length=60, null=True)),
                ('menu_orders_en', models.CharField(default='سفارشات', max_length=60, null=True)),
                ('menu_address', models.CharField(default='آدرس', max_length=60)),
                ('menu_address_fa', models.CharField(default='آدرس', max_length=60, null=True)),
                ('menu_address_en', models.CharField(default='آدرس', max_length=60, null=True)),
                ('menu_profile', models.CharField(default='جزئیات حساب کاربری', max_length=60)),
                ('menu_profile_fa', models.CharField(default='جزئیات حساب کاربری', max_length=60, null=True)),
                ('menu_profile_en', models.CharField(default='جزئیات حساب کاربری', max_length=60, null=True)),
                ('menu_password_change', models.CharField(default='تغییر گذرواژه', max_length=60)),
                ('menu_password_change_fa', models.CharField(default='تغییر گذرواژه', max_length=60, null=True)),
                ('menu_password_change_en', models.CharField(default='تغییر گذرواژه', max_length=60, null=True)),
                ('menu_logout', models.CharField(default='خروج از حساب کاربری', max_length=60)),
                ('menu_logout_fa', models.CharField(default='خروج از حساب کاربری', max_length=60, null=True)),
                ('menu_logout_en', models.CharField(default='خروج از حساب کاربری', max_length=60, null=True)),
                ('header_background', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='profile_background', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PasswordResetPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
                ('title_fa', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('title_en', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('text_head', models.CharField(default='did you forget your password?', max_length=200)),
                ('text_head_fa', models.CharField(default='did you forget your password?', max_length=200, null=True)),
                ('text_head_en', models.CharField(default='did you forget your password?', max_length=200, null=True)),
                ('text_help', models.CharField(default='enter your email to reset your password', max_length=200)),
                ('text_help_fa', models.CharField(default='enter your email to reset your password', max_length=200, null=True)),
                ('text_help_en', models.CharField(default='enter your email to reset your password', max_length=200, null=True)),
                ('password_sent_message', models.TextField(default="We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with,and check your spam folder.", max_length=300)),
                ('password_sent_message_fa', models.TextField(default="We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with,and check your spam folder.", max_length=300, null=True)),
                ('password_sent_message_en', models.TextField(default="We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with,and check your spam folder.", max_length=300, null=True)),
                ('background_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='password_reset_page', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField()),
                ('customer_name', models.CharField(max_length=60)),
                ('picture', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='customer', to=settings.FILER_IMAGE_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=60)),
                ('picture', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='brand_image', to=settings.FILER_IMAGE_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AboutUsPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
                ('title_fa', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('title_en', models.CharField(default='Sepimo', max_length=60, null=True)),
                ('is_brand_active', models.BooleanField(default=False)),
                ('brand_title', models.CharField(max_length=100)),
                ('brand_title_fa', models.CharField(max_length=100, null=True)),
                ('brand_title_en', models.CharField(max_length=100, null=True)),
                ('brand_description', tinymce.models.HTMLField()),
                ('brand_description_fa', tinymce.models.HTMLField(null=True)),
                ('brand_description_en', tinymce.models.HTMLField(null=True)),
                ('our_vision_text', tinymce.models.HTMLField()),
                ('our_vision_text_fa', tinymce.models.HTMLField(null=True)),
                ('our_vision_text_en', tinymce.models.HTMLField(null=True)),
                ('our_mission_text', tinymce.models.HTMLField()),
                ('our_mission_text_fa', tinymce.models.HTMLField(null=True)),
                ('our_mission_text_en', tinymce.models.HTMLField(null=True)),
                ('who_we_are_text_1', tinymce.models.HTMLField()),
                ('who_we_are_text_1_fa', tinymce.models.HTMLField(null=True)),
                ('who_we_are_text_1_en', tinymce.models.HTMLField(null=True)),
                ('who_we_are_text_2', tinymce.models.HTMLField()),
                ('who_we_are_text_2_fa', tinymce.models.HTMLField(null=True)),
                ('who_we_are_text_2_en', tinymce.models.HTMLField(null=True)),
                ('customer_reviews_title', models.CharField(default='نظرات مشتری های فروشگاه', max_length=100)),
                ('main_picture', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='about_us', to=settings.FILER_IMAGE_MODEL)),
                ('who_we_are_picture', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='who_we_are', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
