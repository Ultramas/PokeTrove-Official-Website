# Generated by Django 4.1.10 on 2024-12-17 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0046_ascention'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ascension',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ascension', models.CharField(max_length=200)),
                ('flavor_text', models.CharField(choices=[('A', 'Ate the forbidden cookies'), ('B', 'Bit the bullet'), ('C', 'Caught in the act'), ('D', "Doordash'd "), ('E', 'Enigma '), ('S', 'Shacked to a galloping horse'), ('X', 'Xyster to the keister'), ('Z', 'Zapperdoodled')], max_length=1)),
                ('reward', models.IntegerField(default=1)),
                ('is_active', models.IntegerField(blank=True, choices=[(1, 'Active'), (0, 'Inactive')], default=1, help_text='1->Active, 0->Inactive', null=True, verbose_name='Set active?')),
                ('final_level', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='necessary_level_to_unlock', to='showcase.level')),
            ],
            options={
                'verbose_name': 'Ascension',
                'verbose_name_plural': 'Ascensions',
            },
        ),
        migrations.DeleteModel(
            name='Ascention',
        ),
    ]