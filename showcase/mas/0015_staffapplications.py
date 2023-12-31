# Generated by Django 3.1.5 on 2021-12-28 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase', '0014_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffApplications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Your discord name & tag.', max_length=100)),
                ('overall_time_check', models.BooleanField()),
                ('previous_role_time_check', models.BooleanField()),
                ('meeting_attendance_check', models.BooleanField()),
                ('strikes_check', models.BooleanField()),
                ('role', models.TextField(help_text='What role are you applying for?')),
                ('why', models.TextField(help_text='Tell us why you want to be a MegaClan Staff Member. Be descriptive.')),
                ('how_better', models.TextField(help_text='Tell us what you will do to make MC better as a staff member.')),
                ('read_requirements', models.BooleanField()),
            ],
        ),
    ]
