# Generated by Django 5.1.6 on 2025-03-07 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0014_clickable'),
    ]

    operations = [
        migrations.AddField(
            model_name='clickable',
            name='sound',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
    ]
