# Generated by Django 4.1.2 on 2022-11-26 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0103_rename_advertisementimage_advertisementbase_advertisement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisementbase',
            name='title',
        ),
        migrations.AddField(
            model_name='advertisementbase',
            name='advertisementtitle',
            field=models.CharField(default=1, help_text='Advertisement title.', max_length=100, verbose_name='advertisement title'),
            preserve_default=False,
        ),
    ]
