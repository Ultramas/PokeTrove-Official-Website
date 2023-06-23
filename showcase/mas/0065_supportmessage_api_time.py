# Generated by Django 3.2.11 on 2022-06-15 05:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0064_supportchat_api_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportmessage',
            name='api_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]