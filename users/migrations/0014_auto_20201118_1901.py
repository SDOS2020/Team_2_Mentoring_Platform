# Generated by Django 3.1.3 on 2020-11-18 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_auto_20201118_1858'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
    ]
