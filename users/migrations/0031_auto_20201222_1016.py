# Generated by Django 3.1.3 on 2020-12-22 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0030_milestone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Prefer not to say')], default=(3, 'Prefer not to say')),
        ),
    ]