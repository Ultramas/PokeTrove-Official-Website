# Generated by Django 4.1.10 on 2024-12-12 03:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('showcase', '0016_alter_monstrosity_options_alter_monstrosity_level_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledetails',
            name='monstrosity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='monster', to=settings.AUTH_USER_MODEL),
        ),
    ]