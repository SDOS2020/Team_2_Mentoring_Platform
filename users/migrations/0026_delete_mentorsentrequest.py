# Generated by Django 3.1.3 on 2020-12-21 20:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_auto_20201221_2001'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MentorSentRequest',
        ),
    ]
