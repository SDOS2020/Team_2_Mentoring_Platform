# Generated by Django 3.1.3 on 2021-01-07 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0047_auto_20210107_1124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accounteducation',
            old_name='details',
            new_name='detail',
        ),
        migrations.RenameField(
            model_name='accountresearchexperience',
            old_name='details',
            new_name='detail',
        ),
    ]