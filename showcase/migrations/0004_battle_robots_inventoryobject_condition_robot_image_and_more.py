# Generated by Django 4.1.10 on 2024-06-22 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0003_remove_battle_robots_remove_experience_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='battle',
            name='robots',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_bot': True}, related_name='battles', to='showcase.robot'),
        ),
        migrations.AddField(
            model_name='inventoryobject',
            name='condition',
            field=models.CharField(choices=[('M', 'Mint'), ('NM', 'Near Mint'), ('MP', 'Moderately Played'), ('HP', 'Heavily Played'), ('D', 'Damaged')], default='M', max_length=2),
        ),
        migrations.AddField(
            model_name='robot',
            name='image',
            field=models.FileField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='battle',
            name='battle_name',
            field=models.CharField(blank=True, help_text='Your name and tag go here.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='battle',
            name='participants',
            field=models.ManyToManyField(blank=True, limit_choices_to={'is_bot': False}, related_name='battles', to='showcase.battleparticipant'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='is_bot',
            field=models.BooleanField(default=True),
        ),
    ]