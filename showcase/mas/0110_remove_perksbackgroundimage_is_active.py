# Generated by Django 4.1.2 on 2022-11-29 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0109_rename_page_imagecarousel_carouselpage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perksbackgroundimage',
            name='is_active',
        ),
    ]
