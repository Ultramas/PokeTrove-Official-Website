# Generated by Django 3.2.11 on 2022-06-15 23:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0068_alter_supportmessage_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportmessage',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 6, 15, 23, 13, 35, 400254)),
        ),
    ]