from django.db import models

# Our libraries
import pytz
from django.utils import timezone


# Create your models here.
class ProcessedData(models.Model):
    node_ID = models.IntegerField()
    fill_level = models.IntegerField()
    weight = models.DecimalField(max_digits=6, decimal_places=2)
    mttc = models.CharField(max_length=50)
    mq2_analog = models.IntegerField()
    mq3_analog = models.IntegerField()
    mq6_analog = models.IntegerField()
    mq2_change = models.DecimalField(max_digits=6, decimal_places=2)
    mq3_change = models.DecimalField(max_digits=6, decimal_places=2)
    mq6_change = models.DecimalField(max_digits=6, decimal_places=2)
    flame = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    zone = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # convert timestamp to your timezone
        utc_timestamp = self.timestamp.replace(tzinfo=pytz.UTC)
        local_timestamp = utc_timestamp.astimezone(timezone.get_current_timezone())

        # set timestamp in your model
        self.timestamp = local_timestamp

        super(ProcessedData, self).save(*args, **kwargs)

    def __str__(self):
        return self.node_ID    

class RawData(models.Model):
    Node_ID = models.IntegerField()
    Ultrasonic_CM = models.IntegerField()
    MQ2_Data = models.IntegerField()
    MQ3_Data = models.IntegerField()
    MQ6_Data = models.IntegerField()
    Flame_Data = models.IntegerField()
    Weight_grams = models.FloatField()
