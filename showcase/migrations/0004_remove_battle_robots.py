# Generated by Django 4.1.10 on 2024-12-08 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0003_battle_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='battle',
            name='robots',
        ),
    ]