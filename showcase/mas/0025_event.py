# Generated by Django 3.1.5 on 2022-01-01 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0024_staffprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Event name goes here.', max_length=100)),
                ('category', models.CharField(help_text='Please let us know what type of event this is (tournament, stage night, etc).', max_length=200)),
                ('description', models.TextField(help_text='Give a brief description of the event.')),
                ('date_and_time', models.DateTimeField(null=True)),
                ('staff_feats', models.TextField(help_text='Let us know of your transcendental feats of making MegaClan a better place.')),
                ('image', models.FileField(help_text='Please provide a cover image for your profile.', upload_to='')),
            ],
        ),
    ]
