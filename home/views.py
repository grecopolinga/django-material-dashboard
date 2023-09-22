from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from admin_material.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout

# region - Our libraries and dependencies

from .models import ProcessedData, RawData
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.utils import timezone
from .serializers import ProcessedDataSerializer, RawDataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import defaultdict
import datetime
import json
import time
import serial
import threading
import pytz

Node1 = {"Node_ID": 1, "Ultrasonic_CM":0, "Ultrasonic_Inch":0, "MQ2_Data":0, "MQ3_Data":0, "MQ6_Data":0, "Flame_Data":0, "Weight_lbs":0}
Node2 = {"Node_ID": 2, "Ultrasonic_CM":0, "Ultrasonic_Inch":0, "MQ2_Data":0, "MQ3_Data":0, "MQ6_Data":0, "Flame_Data":0, "Weight_lbs":0}
Node3 = {"Node_ID": 3, "Ultrasonic_CM":0, "Ultrasonic_Inch":0, "MQ2_Data":0, "MQ3_Data":0, "MQ6_Data":0, "Flame_Data":0, "Weight_lbs":0}
Node4 = {"Node_ID": 4, "Ultrasonic_CM":0, "Ultrasonic_Inch":0, "MQ2_Data":0, "MQ3_Data":0, "MQ6_Data":0, "Flame_Data":0, "Weight_lbs":0}


running = True
previous_time = None
previous_value = None
start_time = None
end_time = None
collected_times = []

# endregion

# region - Pages
# Create your views here.
def index(request):
    # Call the processing() function to generate the context data
    context = processing()

    # Add the 'segment' key to the context
    context['segment'] = 'index'

    # Render the template with the generated context data
    return render(request, 'pages/index.html', context)

def billing(request):
  return render(request, 'pages/billing.html', { 'segment': 'billing' })

def tables(request):
  return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
  return render(request, 'pages/virtual-reality.html', { 'segment': 'vr' })

def rtl(request):
  return render(request, 'pages/rtl.html', { 'segment': 'rtl' })

def notification(request):
  return render(request, 'pages/notifications.html', { 'segment': 'notification' })

def profile(request):
  return render(request, 'pages/profile.html', { 'segment': 'profile' })

# Modified Pages
def navigator(request):
  return render(request, 'pages/navigator.html', { 'segment': 'navigator' }) 

# endregion

# This API endpoint gets the whole array of attributes for each bin ID
@api_view(['GET']) 
def getWeightData(request):
    bin_data = {
        'Bin1': (ProcessedData.objects.filter(node_ID=1).values_list('weight', flat=True)),
        'Bin2': (ProcessedData.objects.filter(node_ID=2).values_list('weight', flat=True)),
        'Bin3': (ProcessedData.objects.filter(node_ID=3).values_list('weight', flat=True)),
        'Bin4': (ProcessedData.objects.filter(node_ID=4).values_list('weight', flat=True)),
    }
    return Response(bin_data)

from django.db.models import Q

@api_view(['GET']) 
def getWeightTimeData(request):
    # Get the startDate and endDate from query parameters (assuming you pass them as query parameters)
    start_date_str = request.GET.get('startDate')
    end_date_str = request.GET.get('endDate')

    # Convert the date strings to datetime objects
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d')
    # Add one day to the end date to make it inclusive
    end_date = end_date + timedelta(days=1)
    bin_data = {
        'Bin1': {
            'timestamps': [timestamp.strftime('%Y-%m-%d') for timestamp in ProcessedData.objects.filter(
                node_ID=1, timestamp__range=(start_date, end_date)).values_list('timestamp', flat=True)],
            'weights': list(ProcessedData.objects.filter(
                Q(node_ID=1) & Q(timestamp__range=(start_date, end_date))).values_list('weight', flat=True)),
        },
        'Bin2': {
            'timestamps': [timestamp.strftime('%Y-%m-%d') for timestamp in ProcessedData.objects.filter(
                node_ID=2, timestamp__range=(start_date, end_date)).values_list('timestamp', flat=True)],
            'weights': list(ProcessedData.objects.filter(
                Q(node_ID=2) & Q(timestamp__range=(start_date, end_date))).values_list('weight', flat=True)),
        },
        'Bin3': {
            'timestamps': [timestamp.strftime('%Y-%m-%d') for timestamp in ProcessedData.objects.filter(
                node_ID=3, timestamp__range=(start_date, end_date)).values_list('timestamp', flat=True)],
            'weights': list(ProcessedData.objects.filter(
                Q(node_ID=3) & Q(timestamp__range=(start_date, end_date))).values_list('weight', flat=True)),
        },
        'Bin4': {
            'timestamps': [timestamp.strftime('%Y-%m-%d') for timestamp in ProcessedData.objects.filter(
                node_ID=4, timestamp__range=(start_date, end_date)).values_list('timestamp', flat=True)],
            'weights': list(ProcessedData.objects.filter(
                Q(node_ID=4) & Q(timestamp__range=(start_date, end_date))).values_list('weight', flat=True)),
        },
    }
    return Response(bin_data)


# This API endpoint gets only 10 elements from the whole array of attributes for each bin ID
@api_view(['GET'])
def getLatestData(request):
    bin_data = {
        'Bin1': ProcessedData.objects.filter(node_ID=1).order_by('-timestamp')[:10].values(),
        'Bin2': ProcessedData.objects.filter(node_ID=2).order_by('-timestamp')[:10].values(),
        'Bin3': ProcessedData.objects.filter(node_ID=3).order_by('-timestamp')[:10].values(),
        'Bin4': ProcessedData.objects.filter(node_ID=4).order_by('-timestamp')[:10].values(),
    }
    return Response(bin_data)    

# @api_view(['POST'])
# def receive_sensor_data(request):
#     global Node1, Node2, Node3, Node4
    
#     if request.method == 'POST':
#         # deserialize the sensor data
#         serializer = RawDataSerializer(data=request.data)
#         if serializer.is_valid():
#             sensor_data = request.data
            
#             #If statement to check what node to store the data
#             node_id = sensor_data.get('Node_ID')
#             if node_id == 1:
#                 node = Node1
#             elif node_id == 2:
#                 node = Node2
#             elif node_id == 3:
#                 node = Node3
#             elif node_id == 4:
#                 node = Node4
#             else:
#                 return Response({'error': 'Invalid node ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
#             node["Node_ID"] = sensor_data.get('Node_ID')
#             node["Ultrasonic_CM"] = sensor_data.get('Ultrasonic_CM')
#             node["MQ2_Data"] = sensor_data.get('MQ2_ppm')
#             node["MQ3_Data"] = sensor_data.get('MQ3_ppm')
#             node["MQ6_Data"] = sensor_data.get('MQ6_ppm')
#             node["Flame_Data"] = sensor_data.get('Flame_Data')
#             node["Weight_lbs"] = sensor_data.get('Weight_lbs')
            
#             processing()
            
#             return Response(serializer.data)
    
#     # return an error response if the request method is not POST
#     return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

active_nodes = defaultdict(dict)

@api_view(['POST'])
def receive_sensor_data(request):
    if request.method == 'POST':
        # Deserialize the sensor data
        serializer = RawDataSerializer(data=request.data)
        if serializer.is_valid():
            sensor_data = serializer.validated_data
            
            # Get the node ID from the sensor data
            node_id = sensor_data.get('Node_ID')
            
            # Check if the node is active
            if node_id not in active_nodes:
                return Response({'error': 'Invalid node ID or inactive node.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Store sensor data in the respective node dictionary
            node = active_nodes[node_id]
            node["Node_ID"] = node_id
            node["Ultrasonic_CM"] = sensor_data.get('Ultrasonic_CM')
            node["MQ2_Data"] = sensor_data.get('MQ2_ppm')
            node["MQ3_Data"] = sensor_data.get('MQ3_ppm')
            node["MQ6_Data"] = sensor_data.get('MQ6_ppm')
            node["Flame_Data"] = sensor_data.get('Flame_Data')
            node["Weight_lbs"] = sensor_data.get('Weight_lbs')
            
            # Perform processing specific to the active node
            processing(node)
            
            return Response(serializer.data)
    
    # Return an error response if the request method is not POST
    return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def get_rate_of_change(value):
    global previous_time, previous_value
    current_time = datetime.datetime.now()
    if previous_time is not None:
        time_diff = (current_time - previous_time).total_seconds()
        value_diff = value - previous_value
        if time_diff > 0:
            return value_diff / time_diff        
    previous_time = current_time
    previous_value = value
    return 0

def Overall_Fill_Level(Fill_Level,Load):
    if Fill_Level > 75:
        US_weight = 0.4
        L_weight = 0.6
    else:
        US_weight = 0.6
        L_weight = 0.4
    Overall = ((US_weight * (Fill_Level/100)) + (L_weight * Load/28))#28kg
    return Overall

def Fill_Level(distance):
    accumulated = 55 - distance
    Fill_Level = (accumulated/55) * 100
    if Fill_Level < 0:
        Fill_Level = 0
    return Fill_Level

def lbs_to_kg(lbs):
    kg = lbs/1000
    if kg < 0:
        return 0
    else:
        return kg 

def MTTC(Fill_Level):
    global start_time, end_time, collected_times
    if Fill_Level > 80:
        if start_time is None:
            start_time = time.time()
    elif Fill_Level < 80 and start_time is not None:
        end_time = time.time()
        time_to_collect = end_time - start_time
        collected_times.append(time_to_collect)
        start_time = None

    if len(collected_times) > 0:
        MTTC = sum(collected_times) / len(collected_times)
    else:
        MTTC = 0
    # Convert seconds to minutes and seconds
    minutes, seconds = divmod(MTTC, 60)
    # Format the time as a string in the minute-seconds format
    MTTC_Converted = "{:02d}m {:05.2f}s".format(int(minutes), seconds)
    return MTTC_Converted

def processing():
    #Fill Level
    Bin1_Fill_Level = Fill_Level(int(Node1["Ultrasonic_CM"]))
    Bin2_Fill_Level = Fill_Level(int(Node2["Ultrasonic_CM"]))
    Bin3_Fill_Level = Fill_Level(int(Node3["Ultrasonic_CM"]))
    Bin4_Fill_Level = Fill_Level(int(Node4["Ultrasonic_CM"]))

    #Weight
    Bin1_Weight = lbs_to_kg(float(Node1["Weight_lbs"]))
    Bin2_Weight = lbs_to_kg(float(Node2["Weight_lbs"]))
    Bin3_Weight = lbs_to_kg(float(Node3["Weight_lbs"]))
    Bin4_Weight = lbs_to_kg(float(Node4["Weight_lbs"]))

    #Mean-Time-to-Collect
    Bin1_MTTC = MTTC(Bin1_Fill_Level)
    Bin2_MTTC = MTTC(Bin2_Fill_Level)
    Bin3_MTTC = MTTC(Bin3_Fill_Level)
    Bin4_MTTC = MTTC(Bin4_Fill_Level)

    #Rate of Change of PPM values
    Bin1_MQ2_Change = get_rate_of_change(float(Node1["MQ2_Data"]))
    Bin1_MQ3_Change = get_rate_of_change(float(Node1["MQ3_Data"]))
    Bin1_MQ6_Change = get_rate_of_change(float(Node1["MQ6_Data"]))

    Bin2_MQ2_Change = get_rate_of_change(float(Node2["MQ2_Data"]))
    Bin2_MQ3_Change = get_rate_of_change(float(Node2["MQ3_Data"]))
    Bin2_MQ6_Change = get_rate_of_change(float(Node2["MQ6_Data"]))
    
    Bin3_MQ2_Change = get_rate_of_change(float(Node3["MQ2_Data"]))
    Bin3_MQ3_Change = get_rate_of_change(float(Node3["MQ3_Data"]))
    Bin3_MQ6_Change = get_rate_of_change(float(Node3["MQ6_Data"]))
    
    Bin4_MQ2_Change = get_rate_of_change(float(Node4["MQ2_Data"]))
    Bin4_MQ3_Change = get_rate_of_change(float(Node4["MQ3_Data"]))
    Bin4_MQ6_Change = get_rate_of_change(float(Node4["MQ6_Data"]))

    ph_tz = pytz.timezone('Asia/Manila')
    # Get the current date and time
    now = timezone.now()
    #For the Fill-level graph
    # Create a datetime object for the start of the current day
    start_of_day = datetime.datetime.combine(datetime.date(2023, 8, 28), datetime.time.min).astimezone()
    end_of_day = datetime.datetime.combine(datetime.date(2023, 8, 28), datetime.time.max).astimezone()
    # Query the database for ProcessedData objects that occurred within the current day
    processed_data = ProcessedData.objects.filter(timestamp__gte=start_of_day, timestamp__lt=end_of_day)
    # Extract the fill level and timestamp data for the filtered ProcessedData objects
    fill_levels = [data.fill_level for data in processed_data]
    bin_ids = [data.node_ID for data in processed_data]
    timestamps = [data.timestamp.astimezone(ph_tz).strftime('%H:%M') for data in processed_data]
    # Pass fill_levels and timestamps as JSON objects
    bin_ids_json = json.dumps(bin_ids)
    fill_levels_json = json.dumps(fill_levels)
    timestamps_json = json.dumps(timestamps)
    #End of code for the Fill-level graph

    #For the MTTC graph
    # Create datetime objects for the start and end of the 7-day period
    end_date = timezone.now()  # Use the current date as the end date
    start_date = end_date - datetime.timedelta(days=6)  # Calculate the start date

    # Query the database for ProcessedData objects within the 7-day period
    mttc_processed_data = ProcessedData.objects.filter(timestamp__range=(start_date, end_date))

    # Extract the MTTC, timestamp, and bin ID data for the filtered ProcessedData objects
    mttc_data = [data.mttc for data in mttc_processed_data]
    mttc_bin_ids = [data.node_ID for data in mttc_processed_data]
    mttc_timestamps = [data.timestamp.astimezone(ph_tz).strftime('%m-%d') for data in mttc_processed_data]

    # Pass bin_ids, mttc_data, and timestamps as JSON objects
    mttc_bin_ids_json = json.dumps(mttc_bin_ids)
    mttc_data_json = json.dumps(mttc_data)
    mttc_timestamps_json = json.dumps(mttc_timestamps)

    #For the weight graph
    # Query the database for ProcessedData objects within the 7-day period
    weight_processed_data = ProcessedData.objects.filter(timestamp__range=(start_date, end_date))
    # Extract the Weight, timestamp, and bin ID data for the filtered ProcessedData objects
    weight_data = [data.weight for data in weight_processed_data]
    weight_data_float = [float(value) for value in weight_data]
    weight_bin_ids = [data.node_ID for data in weight_processed_data]
    weight_timestamps = [data.timestamp.astimezone(ph_tz).strftime('%m-%d') for data in weight_processed_data]

    weight_data_json = json.dumps(weight_data_float)
    weight_bin_ids_json = json.dumps(weight_bin_ids)
    weight_timestamps_json = json.dumps(weight_timestamps)
    context = {
        'Bin1_ID': int(Node1["Node_ID"]),
        'Bin1_Fill_Level': int(Bin1_Fill_Level),
        'Bin1_Weight': "{:.2f}".format(float(Bin1_Weight)),
        'Bin1_MTTC': Bin1_MTTC,
        'Bin1_MQ2_PPM': "{:.2f}".format(float(Node1["MQ2_Data"])),
        'Bin1_MQ3_PPM': "{:.2f}".format(float(Node1["MQ3_Data"])),
        'Bin1_MQ6_PPM': "{:.2f}".format(float(Node1["MQ6_Data"])),
        'Bin1_MQ2_Change': "{:.2f}".format(float(Bin1_MQ2_Change)),
        'Bin1_MQ3_Change': "{:.2f}".format(float(Bin1_MQ3_Change)),
        'Bin1_MQ6_Change': "{:.2f}".format(float(Bin1_MQ6_Change)),
        'Bin1_Flame': int(Node1["Flame_Data"]),
        'start': start_of_day,
        'end': end_of_day, 
        'data': processed_data, 
        'timestamps': timestamps_json, 
        'fill_levels': fill_levels_json,
        'bin_ids': bin_ids_json,
        'mttc_data': mttc_data_json,
        'mttc_bin_ids': mttc_bin_ids_json,
        'mttc_timestamps': mttc_timestamps_json,
        'weight_data': weight_data_json,
        'weight_bin_ids': weight_bin_ids_json,
        'weight_timestamps': weight_timestamps_json,
        
        'Bin2_ID': int(Node2["Node_ID"]),
        'Bin2_Fill_Level': int(Bin2_Fill_Level),
        'Bin2_Weight': "{:.2f}".format(float(Bin2_Weight)),
        'Bin2_MTTC': Bin2_MTTC,
        'Bin2_MQ2_PPM': "{:.2f}".format(float(Node2["MQ2_Data"])),
        'Bin2_MQ3_PPM': "{:.2f}".format(float(Node2["MQ3_Data"])),
        'Bin2_MQ6_PPM': "{:.2f}".format(float(Node2["MQ6_Data"])),
        'Bin2_MQ2_Change': "{:.2f}".format(float(Bin2_MQ2_Change)),
        'Bin2_MQ3_Change': "{:.2f}".format(float(Bin2_MQ3_Change)),
        'Bin2_MQ6_Change': "{:.2f}".format(float(Bin2_MQ6_Change)),
        'Bin2_Flame': int(Node2["Flame_Data"]),
        
        'Bin3_ID': int(Node3["Node_ID"]),
        'Bin3_Fill_Level': int(Bin3_Fill_Level),
        'Bin3_Weight': "{:.2f}".format(float(Bin3_Weight)),
        'Bin3_MTTC': Bin3_MTTC,
        'Bin3_MQ2_PPM': "{:.2f}".format(float(Node3["MQ2_Data"])),
        'Bin3_MQ3_PPM': "{:.2f}".format(float(Node3["MQ3_Data"])),
        'Bin3_MQ6_PPM': "{:.2f}".format(float(Node3["MQ6_Data"])),
        'Bin3_MQ2_Change': "{:.2f}".format(float(Bin3_MQ2_Change)),
        'Bin3_MQ3_Change': "{:.2f}".format(float(Bin3_MQ3_Change)),
        'Bin3_MQ6_Change': "{:.2f}".format(float(Bin3_MQ6_Change)),
        'Bin3_Flame': int(Node3["Flame_Data"]),
        
        'Bin4_ID': int(Node4["Node_ID"]),
        'Bin4_Fill_Level': int(Bin4_Fill_Level),
        'Bin4_Weight': "{:.2f}".format(float(Bin4_Weight)),
        'Bin4_MTTC': Bin4_MTTC,
        'Bin4_MQ2_PPM': "{:.2f}".format(float(Node4["MQ2_Data"])),
        'Bin4_MQ3_PPM': "{:.2f}".format(float(Node4["MQ3_Data"])),
        'Bin4_MQ6_PPM': "{:.2f}".format(float(Node4["MQ6_Data"])),
        'Bin4_MQ2_Change': "{:.2f}".format(float(Bin4_MQ2_Change)),
        'Bin4_MQ3_Change': "{:.2f}".format(float(Bin4_MQ3_Change)),
        'Bin4_MQ6_Change': "{:.2f}".format(float(Bin4_MQ6_Change)),
        'Bin4_Flame': int(Node4["Flame_Data"]),
    }

    #For Bin1
    reading = ProcessedData(
    node_ID = Node1["Node_ID"],
    fill_level= int(Bin1_Fill_Level),
    weight = Bin1_Weight,
    mttc = Bin1_MTTC,
    mq2_ppm = Node1["MQ2_Data"],
    mq3_ppm = Node1["MQ3_Data"],
    mq6_ppm = Node1["MQ6_Data"],
    mq2_change = Bin1_MQ2_Change,
    mq3_change = Bin1_MQ3_Change,
    mq6_change = Bin1_MQ6_Change,
    flame = int(Node1["Flame_Data"]))
    reading.save()

    # For Bin2
    reading2 = ProcessedData(
    node_ID = Node2["Node_ID"],
    fill_level=int(Bin2_Fill_Level),
    weight = Bin2_Weight,
    mttc=Bin2_MTTC,
    mq2_ppm=Node2["MQ2_Data"],
    mq3_ppm=Node2["MQ3_Data"],
    mq6_ppm=Node2["MQ6_Data"],
    mq2_change=Bin2_MQ2_Change,
    mq3_change=Bin2_MQ3_Change,
    mq6_change=Bin2_MQ6_Change,
    flame = int(Node2["Flame_Data"]))
    reading2.save()
    
    # For Bin3
    reading3 = ProcessedData(
    node_ID = Node3["Node_ID"],
    fill_level=int(Bin3_Fill_Level),
    weight = Bin3_Weight,
    mttc=Bin3_MTTC,
    mq2_ppm=Node3["MQ2_Data"],
    mq3_ppm=Node3["MQ3_Data"],
    mq6_ppm=Node3["MQ6_Data"],
    mq2_change=Bin3_MQ2_Change,
    mq3_change=Bin3_MQ3_Change,
    mq6_change=Bin3_MQ6_Change,
    flame = int(Node3["Flame_Data"]))
    reading3.save()
    
    # For Bin4
    reading4 = ProcessedData(
    node_ID = Node4["Node_ID"],
    fill_level=int(Bin4_Fill_Level),
    weight = Bin4_Weight,
    mttc=Bin4_MTTC,
    mq2_ppm=Node4["MQ2_Data"],
    mq3_ppm=Node4["MQ3_Data"],
    mq6_ppm=Node4["MQ6_Data"],
    mq2_change=Bin4_MQ2_Change,
    mq3_change=Bin4_MQ3_Change,
    mq6_change=Bin4_MQ6_Change,
    flame = int(Node4["Flame_Data"]))
    reading4.save()

    return context

def get_recent_sensor_data():
    cutoff_time = timezone.now() - timedelta(hours=24)
    return SensorData.objects.filter(date_time__gte=cutoff_time)
    for data in sensor_data:
        # convert to local timezone
        data.date_time = timezone.localtime(data.date_time)
    return sensor_data      



# region - Authentication
class UserLoginView(LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login/')
    else:
      print("Register failed!")
  else:
    form = RegistrationForm()

  context = { 'form': form }
  return render(request, 'accounts/register.html', context)

def logout_view(request):
  logout(request)
  return redirect('/accounts/login/')

class UserPasswordResetView(PasswordResetView):
  template_name = 'accounts/password_reset.html'
  form_class = UserPasswordResetForm

class UserPasswordResetConfirmView(PasswordResetConfirmView):
  template_name = 'accounts/password_reset_confirm.html'
  form_class = UserSetPasswordForm

class UserPasswordChangeView(PasswordChangeView):
  template_name = 'accounts/password_change.html'
  form_class = UserPasswordChangeForm
# endregion
