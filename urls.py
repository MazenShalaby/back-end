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
    path('appointments-list/<int:patient_id>/', views.appointment_details, name='appointment-details'),
    
    # [5] Bookings
    path('booking-list/', views.bookings_list, name='bookings-list'),
    path('booking-list/<int:doctor_id>/', views.booking_details, name='booking-details'),
    
    
    # [6] Activity Feed
    path('activity-feed/', views.activity_feeds_list, name='activity-feed-list'),
    path('activity-feed/<int:doctor_id>/', views.activity_feed_details, name='activity-feed-details'),

    # Rest auth url
    path('rest-auth', include('rest_framework.urls')),

    # Mahmoud Badr
    path('login/', views.LoginAPI.as_view(), name='api_login'),
    path('previous-history/',views.PreviousHistoryAPI.as_view(), name='previous-history'),
    path('photo-upload/',views.PhotoUploadAPI.as_view(), name='photo_upload'),

]
