# Generated by Django 3.2.13 on 2022-06-17 07:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('core', '0030_auto_20220617_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Sepimo', max_length=60)),
                ('background_image', filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.PROTECT, related_name='signup_page', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]