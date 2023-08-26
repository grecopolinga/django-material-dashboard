from django.contrib import admin
from .models import RawData, ProcessedData

# Register your models here.
admin.site.register(ProcessedData)
admin.site.register(RawData)