# Generated by Django 4.1.4 on 2023-01-02 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_people_politics'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('chatroom', models.CharField(max_length=30)),
                ('entry', models.CharField(max_length=140)),
            ],
        ),
    ]
