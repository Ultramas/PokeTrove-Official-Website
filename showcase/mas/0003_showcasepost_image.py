# Generated by Django 3.1.5 on 2021-11-05 16:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0002_auto_20211105_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='showcasepost',
            name='image',
            field=models.FileField(default=django.utils.timezone.now, upload_to='gallery'),
            preserve_default=False,
        ),
    ]
