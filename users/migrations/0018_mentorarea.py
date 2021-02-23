# Generated by Django 3.1.3 on 2020-12-18 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20201120_0247'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.IntegerField(choices=[(1, 'Artificial Intelligence'), (2, 'Computer Vision'), (3, 'Machine Learning and Data Mining'), (4, 'Natural Language Processing'), (5, 'The Web and Information Retrieval'), (6, 'Computer Architecture'), (7, 'Computer Networks'), (8, 'Computer Security'), (9, 'Databases'), (10, 'Design Automation'), (11, 'Embedded and Real-Time Systems'), (12, 'High-Performance Computing'), (13, 'Mobile Computing'), (14, 'Measurement and Performance Analysis'), (15, 'Operating Systems'), (16, 'Programming Languages'), (17, 'Software Engineering'), (18, 'Algorithms and Complexity'), (19, 'Cryptography'), (20, 'Logic and Verification'), (21, 'Computational Bio and Bioinformatics'), (22, 'Computer Graphics'), (23, 'Economics and Computation'), (24, 'Human-Computer Interaction'), (25, 'Robotics'), (26, 'Visualization')], null=True)),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.mentor')),
            ],
        ),
    ]
