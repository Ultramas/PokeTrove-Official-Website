# Generated by Django 5.1.6 on 2025-03-07 23:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0015_clickable_sound'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='showcase.gamehub'),
        ),
    ]
