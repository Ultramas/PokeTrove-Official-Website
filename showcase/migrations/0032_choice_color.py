# Generated by Django 4.1.10 on 2024-07-21 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0031_spinnerchoicerenders'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='color',
            field=models.CharField(blank=True, choices=[('Gra', 'Gray'), ('Gre', 'Green'), ('Y', 'Yellow'), ('O', 'Orange'), ('R', 'Red'), ('B', 'Black'), ('G', 'Gold')], max_length=3, null=True),
        ),
    ]