from django.urls import path, include
from . import views

urlpatterns = [    
    # [1] Users
    path('users-list/', views.users_list, name='users-list'),
    path('users-list/<int:pk>/', views.user_details, name='user-details'),
    
    # [2] Patients
    path('patients-list/', views.patients_list, name='patients-list'),
    path('patients-list/<int:user_id>/', views.patient_details, name='patient-details'),

    # [3] Doctors
    path('doctors-list/', views.doctors_list, name='doctors-list'),
    path('doctors-list/<int:user_id>/', views.doctor_details, name='doctor-details'),
        
    # [4] Appointements
    path('appointments-list/', views.appointements_list, name='appointments-list'),
    path('appointments-list/<int:doctor_id>/', views.appointment_details, name='appointment-details'),
    
    # [5] DoctorAvailability
    path('doctorav-list/', views.bookings_list, name='doctorav-list'),
    path('doctorav-list/<int:doctor_id>/', views.booking_details, name='doctorav-details'),
    
    # Rest auth url
    path('rest-auth', include('rest_framework.urls')),

    # Badr's Urls
    # [6] Login Api
    path('login/', views.user_login_api_view, name='login-user'),
    
    # [7] PreviousHistory
    path('previous-history/',views.previous_history_api_view, name='previous-history'),
    path('previous-history/<int:sender_id>/',views.previous_history_api_view_details, name='previous-history-details'),
    
    # [8] Photo Upload
    path('photo-upload/',views.PhotoUploadAPI.as_view(), name='photo_upload'),   # Postponed
    
    # [9] Alarm
    path('alarm/',views.AlarmAPIView.as_view(), name='alarm'),

]
