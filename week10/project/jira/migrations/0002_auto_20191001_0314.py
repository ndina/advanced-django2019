# Generated by Django 2.2.5 on 2019-10-01 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Описание задачи'),
        ),
    ]
