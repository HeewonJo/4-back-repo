# Generated by Django 5.1.3 on 2024-12-04 13:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruit', '0003_alter_clubrecruit_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='clubrecruit',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recruit', to=settings.AUTH_USER_MODEL),
        ),
    ]
