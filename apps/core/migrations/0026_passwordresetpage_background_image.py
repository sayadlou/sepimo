# Generated by Django 3.2.13 on 2022-06-17 07:41

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('core', '0025_auto_20220522_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='passwordresetpage',
            name='background_image',
            field=filer.fields.image.FilerImageField(default='', on_delete=django.db.models.deletion.PROTECT, related_name='password_reset_page', to=settings.FILER_IMAGE_MODEL),
            preserve_default=False,
        ),
    ]
