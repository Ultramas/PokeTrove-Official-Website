# Generated by Django 4.1.10 on 2024-12-16 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0042_game_cooldown_game_locked'),
    ]

    operations = [
        migrations.AddField(
            model_name='level',
            name='affiliation',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]