# Generated by Django 3.1.3 on 2020-11-15 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20201109_1345'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenteeExpectedRoleField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Btech'), (2, 'Mtech'), (3, 'PhD'), (4, 'Faculty'), (5, 'Developer')], null=True)),
                ('field', models.IntegerField(choices=[(1, 'CS'), (2, 'ECE'), (3, 'CSD')], null=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.mentee')),
            ],
        ),
        migrations.CreateModel(
            name='MenteeRoleField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Btech'), (2, 'Mtech'), (3, 'PhD'), (4, 'Faculty'), (5, 'Developer')], null=True)),
                ('field', models.IntegerField(choices=[(1, 'CS'), (2, 'ECE'), (3, 'CSD')], null=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.mentee')),
            ],
        ),
        migrations.CreateModel(
            name='MentorExpectedRoleField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Btech'), (2, 'Mtech'), (3, 'PhD'), (4, 'Faculty'), (5, 'Developer')], null=True)),
                ('field', models.IntegerField(choices=[(1, 'CS'), (2, 'ECE'), (3, 'CSD')], null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='MentorRoleField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.IntegerField(choices=[(1, 'Btech'), (2, 'Mtech'), (3, 'PhD'), (4, 'Faculty'), (5, 'Developer')], null=True)),
                ('field', models.IntegerField(choices=[(1, 'CS'), (2, 'ECE'), (3, 'CSD')], null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.mentor')),
            ],
        ),
        migrations.RemoveField(
            model_name='typesofmentor',
            name='mentee',
        ),
        migrations.DeleteModel(
            name='TypesOfMentee',
        ),
        migrations.DeleteModel(
            name='TypesOfMentor',
        ),
    ]
