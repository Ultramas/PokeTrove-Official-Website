# Generated by Django 4.1.10 on 2024-12-15 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0039_lottery_currency_lottery_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lottery',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
