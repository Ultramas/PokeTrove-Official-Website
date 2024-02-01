# Generated by Django 4.1.10 on 2024-01-10 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Rubiaces', max_length=200)),
                ('flavor_text', models.CharField(max_length=200)),
                ('file', models.FileField(null=True, upload_to='', verbose_name='Sprite')),
                ('image_length', models.PositiveIntegerField(blank=True, default=100, help_text='Original length of the advertisement (use for original ratio).', null=True, verbose_name='image length')),
                ('image_width', models.PositiveIntegerField(blank=True, default=100, help_text='Original width of the advertisement (use for original ratio).', null=True, verbose_name='image width')),
                ('mfg_date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('is_active', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True, verbose_name='Set active?')),
            ],
            options={
                'verbose_name': 'PokeTrove Currency',
                'verbose_name_plural': 'PokeTrove Currencies',
            },
        ),
        migrations.CreateModel(
            name='Shuffler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=200)),
                ('file', models.FileField(null=True, upload_to='', verbose_name='File')),
                ('image_length', models.PositiveIntegerField(blank=True, default=100, help_text='Original length of the advertisement (use for original ratio).', null=True, verbose_name='image length')),
                ('image_width', models.PositiveIntegerField(blank=True, default=100, help_text='Original width of the advertisement (use for original ratio).', null=True, verbose_name='image width')),
                ('category', models.CharField(help_text='Type the category of product getting shuffled.', max_length=100)),
                ('heat', models.CharField(blank=True, choices=[('M', 'Mild'), ('S', 'Spicy'), ('F', 'Fiery'), ('W', 'Wild'), ('E', 'Explosive')], max_length=2, null=True)),
                ('mfg_date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('is_active', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True, verbose_name='Set active?')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.pollquestion')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='showcase.choice')),
            ],
            options={
                'verbose_name': 'Shuffle Choice',
                'verbose_name_plural': 'Shuffle Choices',
            },
        ),
    ]