# Generated by Django 5.1.1 on 2024-10-03 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_remove_member_grading_of_wanted_badges_badges_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='badges',
        ),
        migrations.RemoveField(
            model_name='member',
            name='grading_of_wanted_badges_badges',
        ),
        migrations.RemoveField(
            model_name='member',
            name='wanted_badges',
        ),
    ]
