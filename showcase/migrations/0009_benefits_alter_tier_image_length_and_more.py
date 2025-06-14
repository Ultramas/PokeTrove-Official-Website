# Generated by Django 4.2.20 on 2025-05-27 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0008_alter_tier_lower_bound_alter_tier_tier_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('benefit', models.CharField(max_length=200)),
                ('is_active', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True, verbose_name='Set active?')),
            ],
            options={
                'verbose_name': 'Benefit',
                'verbose_name_plural': 'Benefits',
            },
        ),
        migrations.AlterField(
            model_name='tier',
            name='image_length',
            field=models.PositiveIntegerField(blank=True, default=100, help_text='Original length of the image (use for original ratio).', null=True, verbose_name='image length'),
        ),
        migrations.AlterField(
            model_name='tier',
            name='image_width',
            field=models.PositiveIntegerField(blank=True, default=100, help_text='Original width of the image (use for original ratio).', null=True, verbose_name='image width'),
        ),
        migrations.AddField(
            model_name='tier',
            name='benefits',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='showcase.benefits'),
            preserve_default=False,
        ),
    ]
