# Generated by Django 4.1.10 on 2024-08-05 18:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('showcase', '0013_currencyorder_profile_order_profile_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdministrationChangeLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100)),
                ('object_id', models.PositiveIntegerField()),
                ('change_type', models.CharField(max_length=50)),
                ('changed_data', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
