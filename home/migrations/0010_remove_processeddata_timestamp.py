# Generated by Django 4.2.5 on 2023-10-23 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_processeddata_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processeddata',
            name='timestamp',
        ),
    ]
