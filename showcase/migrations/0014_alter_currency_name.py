# Generated by Django 4.1.10 on 2024-07-09 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0013_alter_quickitem_options_item_image_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(default='Rubies', max_length=200),
        ),
    ]