# Generated by Django 4.1.10 on 2024-08-31 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0011_inventoryobject_length_for_resize_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventoryobject',
            name='category',
            field=models.CharField(choices=[('G', 'Gold'), ('P', 'Platinum'), ('E', 'Emerald'), ('D', 'Diamond')], default=1, max_length=2),
            preserve_default=False,
        ),
    ]
