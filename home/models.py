from django.db import models

# Our libraries
import pytz
from django.utils import timezone


# Create your models here.
class ProcessedData(models.Model):
    fill_level = models.IntegerField()
    mttc = models.CharField(max_length=50)
    mq2_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    mq3_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    mq6_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    mq2_change = models.DecimalField(max_digits=6, decimal_places=2)
    mq3_change = models.DecimalField(max_digits=6, decimal_places=2)
    mq6_change = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        # convert timestamp to your timezone
        utc_timestamp = self.timestamp.replace(tzinfo=pytz.UTC)
        local_timestamp = utc_timestamp.astimezone(timezone.get_current_timezone())

        # set timestamp in your model
        self.timestamp = local_timestamp

        super(ProcessedData, self).save(*args, **kwargs)

class RawData(models.Model):
    Node_ID = models.IntegerField()
    Ultrasonic_CM = models.IntegerField()
    MQ2_ppm = models.FloatField()
    MQ3_ppm = models.FloatField()
    MQ6_ppm = models.FloatField()
    Flame_Data = models.IntegerField()
    Weight_lbs = models.FloatField()
