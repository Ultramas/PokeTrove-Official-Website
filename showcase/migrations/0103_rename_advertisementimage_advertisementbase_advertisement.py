# Generated by Django 4.1.2 on 2022-11-26 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0102_rename_image_advertisementbase_advertisementimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisementbase',
            old_name='advertisementimage',
            new_name='advertisement',
        ),
    ]