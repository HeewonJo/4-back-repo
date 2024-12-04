# Generated by Django 5.1.3 on 2024-12-03 15:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
        ('news', '0002_alter_news_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='club',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='club_news', to='clubs.club'),
        ),
        migrations.AddField(
            model_name='news',
            name='club_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
