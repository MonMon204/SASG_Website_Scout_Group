# Generated by Django 5.1.1 on 2024-10-02 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0005_remove_badge_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='badgeterm',
            name='term_name',
        ),
        migrations.AddField(
            model_name='badgeterm',
            name='term',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='badgeterm',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='badgeterm',
            name='grade',
            field=models.TextField(blank=True),
        ),
    ]
