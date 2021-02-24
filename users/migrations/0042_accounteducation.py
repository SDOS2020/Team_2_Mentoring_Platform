# Generated by Django 3.1.3 on 2021-01-07 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_auto_20210107_0115'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountEducation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('education', models.TextField(max_length=512, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.account')),
            ],
        ),
    ]
