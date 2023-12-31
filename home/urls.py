from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.index, name='index'),
    path('billing/', views.billing, name='billing'),
    path('tables/', login_required(views.tables), name='tables'),
    path('vr/', views.vr, name='vr'),
    path('rtl/', views.rtl, name='rtl'),
    path('notification/', views.notification, name='notification'),
    path('profile/', login_required(views.profile), name='profile'),
    
    # Our modified URLS
    path('navigator/', login_required(views.navigator), name='navigator'),
    path('api/getPrioritizationData', views.getPrioritizationData, name='getPrioritizationData'), 
    path('api/getWeightData', views.getWeightData, name='getWeightData'),
    path('api/getWeightTimeData', views.getWeightTimeData, name='getWeightTimeData'),
    path('api/getMTTCData', views.getMTTCData, name='getMTTCData'),
    path('api/getFillLevelData', views.getFillLevelData, name='getFillLevelData'),
    path('api/getRateOfChange', views.getRateOfChange, name='getRateOfChange'),
    path('api/getLatestData', views.getLatestData, name='getLatestData'),
    path('api/sensor-data', views.receive_sensor_data, name='receive_sensor_data'),
    path('api/update_zone/<int:bin_id>/<int:new_zone>/<str:new_location>/', views.update_bin_zone, name='update_bin_zone'),
    path('api/update_zone/<int:bin_id>/<int:new_zone>/', views.update_bin_zone_no_location, name='update_bin_zone_no_location'),
    


    # Authentication
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),
    path('accounts/password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
]
