# Generated by Django 4.1.4 on 2023-01-13 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_alter_chatentry_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatentry',
            name='timestamp',
            field=models.IntegerField(default='', max_length=100),
        ),
    ]
