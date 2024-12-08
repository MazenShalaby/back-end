from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, DoctorsProfileInfo, Appointment,  DoctorAvailableBooking, ActivityFeed, User , PreviousHistory, UploadedPhoto
from .serilaizers import UserProfileSerializer, DoctorInfoSerializer, AppointmentSerializer, DoctorAVailableBookingSerializer, ActivityFeedSerializer, LoginSerializer ,PreviousHistorySerializer, UploadedPhotoSerializer

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .permissions import IsAuthenticatedOrReadonly

# Create your views here.

########################################################################## {Django REST Framework} #########################################################################################################
############################################################################################################################################################################################################
############################################################################################################################################################################################################

class LoginAPI(APIView):
    def get(self, request):
        users = User.objects.all()  
        data = [{"name": user.name, "national_id": user.national_id} for user in users]  
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            national_id = serializer.validated_data['national_id']
            try:
                user = User.objects.get(name=name, national_id=national_id)
                return Response({"message": "Login successful", "redirect": "home"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"message": "User not found", "redirect": "signup"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
####################################################################################################################################################################################################################################################################

class PreviousHistoryAPI(APIView):
    def get(self, request):
        histories = PreviousHistory.objects.all().order_by('id')
        serializer = PreviousHistorySerializer(histories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PreviousHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#####################################################################################################################################################################################################################################

class PhotoUploadAPI(APIView):
    def get(self, request):
        photos = UploadedPhoto.objects.all()
        serializer = UploadedPhotoSerializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):  # Ensure format=None for file uploads
        serializer = UploadedPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

############################################################## [1] User Registerations ##############################################################
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def users_list(request):
    if request.method == "GET":
        users = UserProfile.objects.all()
        serializers = UserProfileSerializer(users, many=True)
        return Response(serializers.data)
    
    elif request.method == "POST":
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# [1.1] ==> Specific User Details 

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_details(request, pk):
    
    user = UserProfile.objects.get(id=pk)
    if request.method == 'GET':
        serializer = UserProfileSerializer(user, many = False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "Item deleted successfully"})

############################################################## [2] List of Available Doctors ##############################################################

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def doctors_list(request):
    
    if request.method == 'GET':
        doctors = DoctorsProfileInfo.objects.all()
        serializer = DoctorInfoSerializer(doctors, many=True)
        return Response(serializer.data)
    
# [2.1] ==>  Specific Details 

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def doctor_details(request, pk):
    
    doctors = DoctorsProfileInfo.objects.get(id=pk)
    
    if request.method == 'GET':
        serializer = DoctorInfoSerializer(doctors, many=False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = DoctorInfoSerializer(doctors, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        doctors.delete()
        return Response({"message": "Item deleted successfully !"})
    return Response({"error": "Doctor are not found"}, status=404)
    
    
############################################################## [3] Patients Appointments ##############################################################

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def appointements_list(request):
    
    if request.method == 'GET':
        appointment = Appointment.objects.all()
        serializer = AppointmentSerializer(appointment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AppointmentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "An appointment has been added successfully :) "}, status= status.HTTP_201_CREATED)
        
    return Response({"message": "Something went wrong to delete :( "}, status=status.HTTP_400_BAD_REQUEST)

# [3.1] ==> Specific Patient Appointment

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def appointment_details(request, pk):
    detail = Appointment.objects.get(id=pk)

    if request.method == "GET":
        serializer = AppointmentSerializer(detail, many = False)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AppointmentSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        detail = Appointment.objects.get(id=pk).delete()
        return Response({"message": "Item deleted successfully"})
    
    return Response({"message": "Something went wrong to delete :( "}, status=status.HTTP_400_BAD_REQUEST)
        

############################################################## [4] Doctors Appointments Avialable or Not ##############################################################

class Generic_Available_Doctors_Appointments_list(generics.ListCreateAPIView):
    queryset = DoctorAvailableBooking.objects.all()
    serializer_class = DoctorAVailableBookingSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]


class Generic_Generic_Available_Doctors_Appointments_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = DoctorAvailableBooking.objects.all()
    serializer_class = DoctorAVailableBookingSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    

############################################################## [5] Activity Feed ##############################################################

class Generic_Activity_Feed(generics.ListCreateAPIView):
    queryset = ActivityFeed.objects.all()
    serializer_class = ActivityFeedSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    
class Generic_Activity_Feed_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = ActivityFeed.objects.all()
    serializer_class = ActivityFeedSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    
################################################################################################################################################################################################################################################################################################################################






