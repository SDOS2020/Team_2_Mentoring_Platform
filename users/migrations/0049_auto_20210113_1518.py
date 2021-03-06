# Generated by Django 3.1.3 on 2021-01-13 09:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0048_auto_20210107_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='age',
            field=models.IntegerField(default=20, null=True, validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='menteeexpectedrolefield',
            name='field',
            field=models.IntegerField(choices=[(1, 'Computer Science and Engineering'), (2, 'Electronics and Communication Engineering'), (3, 'Computer Science and Design'), (4, 'Computer Science and Mathematics'), (5, 'Computer Science and Social Sciences'), (6, 'Computer Science and Artificial Intelligence')], null=True),
        ),
        migrations.AlterField(
            model_name='menteeexpectedrolefield',
            name='role',
            field=models.IntegerField(choices=[(1, 'Faculty'), (2, 'Industry Researcher'), (3, 'BTech'), (4, 'MTech'), (5, 'PhD')], null=True),
        ),
        migrations.AlterField(
            model_name='menteerolefield',
            name='field',
            field=models.IntegerField(choices=[(1, 'Computer Science and Engineering'), (2, 'Electronics and Communication Engineering'), (3, 'Computer Science and Design'), (4, 'Computer Science and Mathematics'), (5, 'Computer Science and Social Sciences'), (6, 'Computer Science and Artificial Intelligence')], null=True),
        ),
        migrations.AlterField(
            model_name='menteerolefield',
            name='role',
            field=models.IntegerField(choices=[(1, 'Faculty'), (2, 'Industry Researcher'), (3, 'BTech'), (4, 'MTech'), (5, 'PhD')], null=True),
        ),
        migrations.AlterField(
            model_name='mentorexpectedrolefield',
            name='field',
            field=models.IntegerField(choices=[(1, 'Computer Science and Engineering'), (2, 'Electronics and Communication Engineering'), (3, 'Computer Science and Design'), (4, 'Computer Science and Mathematics'), (5, 'Computer Science and Social Sciences'), (6, 'Computer Science and Artificial Intelligence')], null=True),
        ),
        migrations.AlterField(
            model_name='mentorexpectedrolefield',
            name='role',
            field=models.IntegerField(choices=[(1, 'Faculty'), (2, 'Industry Researcher')], null=True),
        ),
        migrations.AlterField(
            model_name='mentorrolefield',
            name='field',
            field=models.IntegerField(choices=[(1, 'Computer Science and Engineering'), (2, 'Electronics and Communication Engineering'), (3, 'Computer Science and Design'), (4, 'Computer Science and Mathematics'), (5, 'Computer Science and Social Sciences'), (6, 'Computer Science and Artificial Intelligence')], null=True),
        ),
        migrations.AlterField(
            model_name='mentorrolefield',
            name='role',
            field=models.IntegerField(choices=[(1, 'Faculty'), (2, 'Industry Researcher')], null=True),
        ),
    ]
