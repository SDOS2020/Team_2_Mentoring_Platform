# Generated by Django 3.1.3 on 2021-01-13 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0050_auto_20210113_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingsummary',
            name='meeting_length',
            field=models.FloatField(),
        ),
    ]
