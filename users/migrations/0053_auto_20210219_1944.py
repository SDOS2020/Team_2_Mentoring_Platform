# Generated by Django 3.1.3 on 2021-02-19 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0052_rejectedmentorshiprequest'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rejectedmentorshiprequest',
            old_name='date_ended',
            new_name='date_rejected',
        ),
        migrations.RenameField(
            model_name='rejectedmentorshiprequest',
            old_name='end_reason',
            new_name='reject_reason',
        ),
    ]
