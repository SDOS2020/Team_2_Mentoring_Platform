# Generated by Django 3.1.3 on 2020-11-19 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_meeting'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='meeting_url',
            field=models.CharField(default='https://www.meet.google.com', max_length=128),
        ),
    ]