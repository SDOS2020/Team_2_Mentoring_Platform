# Generated by Django 3.1.3 on 2021-01-13 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0049_auto_20210113_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.IntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Prefer not to say')], default=3),
        ),
    ]
