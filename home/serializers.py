from rest_framework import serializers
from .models import ProcessedData, RawData

class RawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawData
        fields = ('Node_ID','Ultrasonic_CM','MQ2_ppm', 'MQ3_ppm', 'MQ6_ppm', 'Flame_Data', 'Weight_lbs')
        
class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessedData
        fields = ('node_id', 'fill_level','mttc','mq2_ppm', 'mq3_ppm', 'mq6_ppm', 'mq2_change', 'mq3_change', 'mq6_change', 'timestamp')