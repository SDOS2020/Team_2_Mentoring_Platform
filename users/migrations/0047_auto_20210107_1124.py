# Generated by Django 3.1.3 on 2021-01-07 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0046_auto_20210107_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='education',
        ),
        migrations.RemoveField(
            model_name='account',
            name='research_experience',
        ),
    ]
