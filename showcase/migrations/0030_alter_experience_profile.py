# Generated by Django 4.1.10 on 2024-12-14 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0029_rename_earned_experience_level_experience_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='showcase.profiledetails'),
        ),
    ]