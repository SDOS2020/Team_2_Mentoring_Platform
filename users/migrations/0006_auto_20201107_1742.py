# Generated by Django 3.1.3 on 2020-11-07 17:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201107_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='age',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='account',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
