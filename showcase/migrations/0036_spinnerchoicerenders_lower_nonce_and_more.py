# Generated by Django 4.1.10 on 2024-07-26 18:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0035_remove_outcome_image_outcome_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='spinnerchoicerenders',
            name='lower_nonce',
            field=models.DecimalField(blank=True, decimal_places=0, help_text='Lower bound nonce of Choice', max_digits=7, null=True, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='spinnerchoicerenders',
            name='upper_nonce',
            field=models.DecimalField(blank=True, decimal_places=0, help_text='Upper bound nonce of Choice', max_digits=7, null=True, validators=[django.core.validators.MaxValueValidator(1000000), django.core.validators.MinValueValidator(0)]),
        ),
    ]