# Generated by Django 4.1.10 on 2024-08-31 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0013_tradeitem_certified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryobject',
            name='choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='showcase.choice'),
        ),
    ]