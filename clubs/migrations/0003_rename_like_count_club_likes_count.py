# Generated by Django 5.1.3 on 2024-11-30 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_alter_club_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='club',
            old_name='like_count',
            new_name='likes_count',
        ),
    ]
