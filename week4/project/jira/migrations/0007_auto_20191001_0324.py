# Generated by Django 2.2.5 on 2019-10-01 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira', '0006_auto_20191001_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskdocument',
            name='document',
            field=models.FileField(upload_to='jira/documents/', verbose_name='Документ'),
        ),
    ]
