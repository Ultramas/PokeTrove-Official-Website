# Generated by Django 4.1.10 on 2024-12-24 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0068_rename_prize_exchangeprize_choice_text_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exchangeprize',
            old_name='choice_text',
            new_name='prize',
        ),
    ]