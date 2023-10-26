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
    mq2_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    mq3_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    mq6_ppm = models.DecimalField(max_digits=6, decimal_places=2)
    mq2_change = models.DecimalField(max_digits=6, decimal_places=2)
    mq3_change = models.DecimalField(max_digits=6, decimal_places=2)
    mq6_change = models.DecimalField(max_digits=6, decimal_places=2)
    flame = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    zone = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        if not self.timestamp.tzinfo:
            # Convert to "Asia/Manila" timezone
            manila_timezone = timezone.pytz.timezone("Asia/Manila")
            self.timestamp = manila_timezone.localize(self.timestamp)

class RawData(models.Model):
    Node_ID = models.IntegerField()
    Ultrasonic_CM = models.IntegerField()
    MQ2_ppm = models.FloatField()
    MQ3_ppm = models.FloatField()
    MQ6_ppm = models.FloatField()
    Flame_Data = models.IntegerField()
    Weight_lbs = models.FloatField()
