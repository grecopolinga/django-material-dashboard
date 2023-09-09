# Generated by Django 4.2.4 on 2023-08-26 11:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fill_level', models.IntegerField()),
                ('mttc', models.CharField(max_length=50)),
                ('mq2_ppm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('mq3_ppm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('mq6_ppm', models.DecimalField(decimal_places=2, max_digits=6)),
                ('mq2_change', models.DecimalField(decimal_places=2, max_digits=6)),
                ('mq3_change', models.DecimalField(decimal_places=2, max_digits=6)),
                ('mq6_change', models.DecimalField(decimal_places=2, max_digits=6)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Node_ID', models.IntegerField()),
                ('Ultrasonic_CM', models.IntegerField()),
                ('MQ2_ppm', models.FloatField()),
                ('MQ3_ppm', models.FloatField()),
                ('MQ6_ppm', models.FloatField()),
                ('Flame_Data', models.IntegerField()),
                ('Weight_lbs', models.FloatField()),
            ],
        ),
    ]