# Generated by Django 3.2.13 on 2022-06-17 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20220617_1217'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PasswordChangePage',
            new_name='BlogPage',
        ),
        migrations.DeleteModel(
            name='PasswordChangeDonePage',
        ),
    ]
