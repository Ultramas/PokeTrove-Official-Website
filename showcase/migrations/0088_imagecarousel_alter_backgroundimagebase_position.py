# Generated by Django 4.1.2 on 2022-11-07 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0087_accountbackgroundimage_addonsbackgroundimage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Your name goes here.', max_length=100)),
                ('caption', models.TextField(help_text='Caption for the image.')),
                ('image', models.ImageField(help_text='Link a URL for your profile (scales to your picture`s dimensions.)', upload_to='')),
                ('position', models.IntegerField(help_text='Positioning of image.')),
                ('page', models.TextField(verbose_name='Page Name')),
                ('is_active', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True)),
            ],
            options={
                'verbose_name': 'Image Carousel Post',
                'verbose_name_plural': 'Image Carousel Posts',
            },
        ),
        migrations.AlterField(
            model_name='backgroundimagebase',
            name='position',
            field=models.IntegerField(verbose_name='Image Position'),
        ),
    ]