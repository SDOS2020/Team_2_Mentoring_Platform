# Generated by Django 3.1.3 on 2020-12-31 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_merge_20201222_1617'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='experience',
            new_name='research_experience',
        ),
    ]
