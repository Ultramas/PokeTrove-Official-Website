# Generated by Django 4.1.10 on 2024-12-14 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0030_alter_experience_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='level',
            field=models.ManyToManyField(blank=True, null=True, related_name='current_level', to='showcase.level'),
        ),
    ]