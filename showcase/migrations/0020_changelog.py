# Generated by Django 4.2.20 on 2025-06-01 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('showcase', '0019_clickable_lore'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete')], max_length=6)),
                ('model', models.CharField(max_length=100)),
                ('object_id', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('changes', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Changelog',
                'verbose_name_plural': 'Changelogs',
            },
        ),
    ]
