# Generated by Django 4.1.10 on 2024-08-30 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0008_rename_value_commerceexchange_total_prize_value_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='condition',
            field=models.CharField(blank=True, choices=[('M', 'Mint'), ('NM', 'Near Mint'), ('MP', 'Moderately Played'), ('HP', 'Heavily Played'), ('D', 'Damaged')], default='M', max_length=2, null=True),
        ),
    ]
