# Generated by Django 4.1.2 on 2022-11-25 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0095_banappealbackgroundimage_punishappsbackgroundimage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='basecopyrighttextfield',
            name='is_active',
            field=models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True),
        ),
    ]