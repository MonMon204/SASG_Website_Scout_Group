# Generated by Django 5.1.1 on 2024-10-06 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_remove_gallery_file_remove_gallery_file_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
