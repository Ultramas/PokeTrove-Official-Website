# Generated by Django 3.1.5 on 2022-01-14 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0037_item_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkoutaddress',
            options={'verbose_name': 'Checkout Address', 'verbose_name_plural': 'Checkout Addresses'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Order Item', 'verbose_name_plural': 'Order Items'},
        ),
        migrations.AlterModelOptions(
            name='reportissue',
            options={'verbose_name': 'Report Issue', 'verbose_name_plural': 'Report Issues'},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(help_text='Link an image for your idea (scales to your picture`s dimensions.)', upload_to=''),
        ),
        migrations.AlterField(
            model_name='poste',
            name='image',
            field=models.ImageField(help_text='Link an image for your profile (scales to your picture`s dimensions.)', upload_to=''),
        ),
        migrations.AlterField(
            model_name='showcasepost',
            name='image',
            field=models.ImageField(help_text='Link an image for your profile (scales to your picture`s dimensions.)', upload_to=''),
        ),
    ]