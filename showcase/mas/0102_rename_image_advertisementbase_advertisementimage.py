# Generated by Django 4.1.2 on 2022-11-26 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0101_alter_advertisementbase_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='advertisementbase',
            old_name='image',
            new_name='advertisementimage',
        ),
    ]
