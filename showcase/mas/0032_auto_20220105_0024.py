# Generated by Django 3.1.5 on 2022-01-05 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0031_auto_20220104_1818'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banappeal',
            options={'verbose_name': 'Ban Appeal', 'verbose_name_plural': 'Ban Appeals'},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'Cities'},
        ),
        migrations.AlterModelOptions(
            name='newsfeed',
            options={'verbose_name': 'News Feed', 'verbose_name_plural': 'News Feed'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'Idea', 'verbose_name_plural': 'Ideas'},
        ),
        migrations.AlterModelOptions(
            name='poste',
            options={'verbose_name': 'Vote', 'verbose_name_plural': 'Votes'},
        ),
        migrations.AlterModelOptions(
            name='punishappeal',
            options={'verbose_name': 'Punish Appeal', 'verbose_name_plural': 'Punishment Appeals'},
        ),
        migrations.AlterModelOptions(
            name='showcasepost',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterModelOptions(
            name='staffapplication',
            options={'verbose_name': 'Staff Application', 'verbose_name_plural': 'Staff Applications'},
        ),
        migrations.AlterModelOptions(
            name='staffprofile',
            options={'verbose_name': 'Staff Profile', 'verbose_name_plural': 'Staff Profiles'},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.URLField(help_text='Link a URL for your idea (scales to your picture`s dimensions.)'),
        ),
        migrations.AlterField(
            model_name='poste',
            name='category',
            field=models.CharField(help_text='Type the category that you are voting on (server layout, event idea, administration position, etc).', max_length=100),
        ),
    ]
