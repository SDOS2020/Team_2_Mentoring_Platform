# Generated by Django 3.1.3 on 2021-01-07 11:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_auto_20210107_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounteducation',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounteducation',
            name='organization',
            field=models.CharField(default='msft', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounteducation',
            name='qualification',
            field=models.CharField(default='haha', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounteducation',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountresearchexperience',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountresearchexperience',
            name='organization',
            field=models.CharField(default='msft', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountresearchexperience',
            name='position',
            field=models.CharField(default='janitor', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accountresearchexperience',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]