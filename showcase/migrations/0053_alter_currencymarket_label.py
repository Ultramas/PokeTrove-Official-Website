# Generated by Django 4.1.10 on 2024-01-29 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0052_currencymarket_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencymarket',
            name='label',
            field=models.CharField(blank=True, choices=[('N', 'New'), ('BS', 'Best Seller'), ('BV', 'Best Value')], max_length=1000, null=True),
        ),
    ]