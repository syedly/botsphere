# Generated by Django 5.0.4 on 2025-02-01 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0010_audiofile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AudioFile',
        ),
    ]
