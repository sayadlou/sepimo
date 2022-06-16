# Generated by Django 3.2.13 on 2022-05-19 07:57

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='intro_picture',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='blog_intro', to=settings.FILER_IMAGE_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture_content',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='blog_content', to=settings.FILER_IMAGE_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture_header',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='blog_header', to=settings.FILER_IMAGE_MODEL),
        ),
    ]