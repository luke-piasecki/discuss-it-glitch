# Generated by Django 4.1.4 on 2023-01-02 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_alter_chatentry_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatentry',
            name='username',
        ),
        migrations.AddField(
            model_name='chatentry',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]