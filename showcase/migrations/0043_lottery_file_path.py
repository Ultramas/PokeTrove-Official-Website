# Generated by Django 4.1.10 on 2024-01-25 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0042_lottery_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='lottery',
            name='file_path',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]