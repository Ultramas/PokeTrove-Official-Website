# Generated by Django 4.1.10 on 2024-08-03 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0008_tradecontract_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='currencyorderprice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='orderprice',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='itemhistory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='showcase.item', verbose_name='Order history'),
        ),
    ]