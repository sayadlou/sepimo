# Generated by Django 3.2.13 on 2022-05-19 08:00

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('core', '0023_auto_20220519_1218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutuspage',
            name='main_picture',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='about_us', to=settings.FILER_IMAGE_MODEL),
        ),
    ]