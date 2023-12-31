# Generated by Django 4.1.2 on 2022-11-29 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0110_remove_perksbackgroundimage_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='perksbackgroundimage',
            name='is_active',
            field=models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True, verbose_name='Set active?'),
        ),
    ]
