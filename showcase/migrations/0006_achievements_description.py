# Generated by Django 4.1.10 on 2024-07-30 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0005_achievements_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievements',
            name='description',
            field=models.TextField(default=1, verbose_name='Description'),
            preserve_default=False,
        ),
    ]