# Generated by Django 4.1.4 on 2023-01-09 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_people_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatrooms',
            name='chat_log',
            field=models.CharField(default='', max_length=28000),
        ),
    ]
