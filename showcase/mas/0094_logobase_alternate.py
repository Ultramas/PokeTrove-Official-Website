# Generated by Django 4.1.2 on 2022-11-17 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0093_remove_logobase_url_logobase_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='logobase',
            name='alternate',
            field=models.TextField(default=1, verbose_name='Alternate Text'),
            preserve_default=False,
        ),
    ]
