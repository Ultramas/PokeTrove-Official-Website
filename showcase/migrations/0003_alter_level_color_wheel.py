# Generated by Django 5.1.6 on 2025-02-28 04:19

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_card'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='color_wheel',
            field=colorfield.fields.ColorField(blank=True, default=None, image_field=None, max_length=25, null=True, samples=[('#FFFFFF', 'white'), ('#000000', 'black')]),
        ),
    ]
