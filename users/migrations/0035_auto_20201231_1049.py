# Generated by Django 3.1.3 on 2020-12-31 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0034_auto_20201231_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='mentor',
            name='will_mentor_btech',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mentor',
            name='will_mentor_faculty',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mentor',
            name='will_mentor_mtech',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='mentor',
            name='will_mentor_phd',
            field=models.BooleanField(default=False),
        ),
    ]
