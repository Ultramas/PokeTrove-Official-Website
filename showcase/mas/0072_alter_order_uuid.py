# Generated by Django 3.2.11 on 2022-06-22 20:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0071_auto_20220622_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False),
        ),
    ]
