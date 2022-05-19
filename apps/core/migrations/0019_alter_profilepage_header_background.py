# Generated by Django 3.2.13 on 2022-05-19 06:16

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('core', '0018_rename_header_text_background_profilepage_header_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepage',
            name='header_background',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.CASCADE, related_name='profile_background', to=settings.FILER_IMAGE_MODEL),
        ),
    ]
