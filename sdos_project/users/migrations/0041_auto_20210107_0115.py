# Generated by Django 3.1.3 on 2021-01-06 19:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0040_deletedmentormenteerelation_date_ended'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletedmentormenteerelation',
            name='date_ended',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
