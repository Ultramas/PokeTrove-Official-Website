# Generated by Django 4.1.10 on 2024-07-05 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0008_alter_message_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]