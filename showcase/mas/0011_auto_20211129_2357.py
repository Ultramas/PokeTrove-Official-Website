# Generated by Django 3.1.5 on 2021-11-29 23:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0010_auto_20211129_0530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mymodel',
            name='description',
        ),
        migrations.RemoveField(
            model_name='mymodel',
            name='name',
        ),
        migrations.AddField(
            model_name='mymodel',
            name='password',
            field=models.SlugField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
