# Generated by Django 4.1.2 on 2022-11-26 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0100_advertisementbase_delete_advertisementpost'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisementbase',
            options={'verbose_name': 'Advertisement Base', 'verbose_name_plural': 'Advertisement Base'},
        ),
    ]