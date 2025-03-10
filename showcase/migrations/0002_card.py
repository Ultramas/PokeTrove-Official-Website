# Generated by Django 5.1.6 on 2025-02-27 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('supertype', models.CharField(max_length=50)),
                ('subtypes', models.CharField(max_length=100)),
                ('hp', models.CharField(blank=True, max_length=10, null=True)),
                ('types', models.CharField(blank=True, max_length=100, null=True)),
                ('evolves_to', models.CharField(blank=True, max_length=100, null=True)),
                ('rules', models.TextField(blank=True, null=True)),
                ('attacks', models.TextField(blank=True, null=True)),
                ('weaknesses', models.TextField(blank=True, null=True)),
                ('retreat_cost', models.CharField(blank=True, max_length=50, null=True)),
                ('set_name', models.CharField(max_length=100)),
                ('set_series', models.CharField(max_length=100)),
                ('set_release_date', models.DateField(blank=True, null=True)),
                ('image_small', models.URLField()),
                ('image_large', models.URLField()),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
            ],
        ),
    ]
