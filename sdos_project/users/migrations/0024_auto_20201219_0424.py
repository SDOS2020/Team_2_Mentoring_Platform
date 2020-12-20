# Generated by Django 3.1.3 on 2020-12-18 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20201219_0327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='designation',
        ),
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Prefer not to say')], default=(3, 'Prefer not to say'), max_length=1),
        ),
    ]
