# Generated by Django 4.2.5 on 2023-10-18 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_mq2_ppm_rawdata_mq2_data_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rawdata',
            old_name='Weight_lbs',
            new_name='Weight_grams',
        ),
    ]
