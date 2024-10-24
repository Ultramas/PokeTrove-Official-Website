# Generated by Django 4.1.10 on 2024-08-30 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0009_choice_condition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradeitem',
            name='choice',
        ),
        migrations.AddField(
            model_name='tradeitem',
            name='inventoryobject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='showcase.inventoryobject'),
        ),
    ]