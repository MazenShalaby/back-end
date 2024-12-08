from django.urls import path, include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [    
    # [1] Users
    path('users-list/', views.users_list, name='users-list'),
    path('users-list/<str:pk>/', views.user_details, name='user-details'),

    # [2] Doctors
    path('doctors-list/', views.doctors_list, name='doctors-list'),
    path('doctors-list/<str:pk>/', views.doctor_details, name='doctor-details'),
    
    # [3] Appointements
    path('appointments-list/', views.appointements_list, name='appointments-list'),
    path('appointments-list/<str:pk>/', views.appointment_details, name='appointment-details'),
    
    # [4] Doctors Available Appointment
    path('available-doctors/',views.Generic_Available_Doctors_Appointments_list().as_view()),
    path('available-doctors/<str:pk>/',views.Generic_Generic_Available_Doctors_Appointments_pk.as_view()),
    
    
    # [5] Activity Feed
    path('activity-feed/', views.Generic_Activity_Feed.as_view()),
    path('activity-feed/<str:pk>/', views.Generic_Activity_Feed_pk.as_view()),

    # Rest auth url
    path('rest-auth', include('rest_framework.urls')),

    # Token auth url
    path('api-token-auth/', obtain_auth_token),
    
    
    
    
    path('login/', views.LoginAPI.as_view(), name='api_login'),
    path('previous-history/',views.PreviousHistoryAPI.as_view(), name='previous-history'),
    path('photo-upload/',views.PhotoUploadAPI.as_view(), name='photo_upload'),

    

]