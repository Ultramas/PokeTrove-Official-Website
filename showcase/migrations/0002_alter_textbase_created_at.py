# Generated by Django 4.1.10 on 2023-10-11 17:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textbase',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
