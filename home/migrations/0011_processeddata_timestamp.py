# Generated by Django 4.2.5 on 2023-10-23 13:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_remove_processeddata_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='processeddata',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
