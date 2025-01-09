from .models import User, Profile, DoctorsProfileInfo, Appointment, DoctorAvailability, UserLogin, PreviousHistory, UploadedPhoto, Alarm
from .serilaizers import  (UserSerializer, ProfileSerializer, DoctorInfoSerializer, AppointmentSerializer, DoctorAvailabilitySerializer,
LoginSerializer , PreviousHistorySerializer, UploadedPhotoSerializer, AlarmSerializer)

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login  # To handle model validation errors

# Create your views here.

########################################################################## {Django REST Framework} #########################################################################################################

################################################################################# [1] Users ###############################################################################################################################################################################################################################################
# [1.1] ==> User(s) List
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def users_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Password will be hashed by the serializer
            retrieved_user = User.objects.get(pk=user.pk)  # Fetch full instance for response
            retrieved_serializer = UserSerializer(retrieved_user)
            return Response(retrieved_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# [1.2] ==> Specific User Details
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_details(request, pk):
    try:
        # Fetch the profile based on the user_id
        profile = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    user = User.objects.get(id=pk)
    if request.method == 'GET':
        serializer = UserSerializer(user, many = False)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "User deleted successfully"})
    
############################################################## [2] Patients ##############################################################
# [2.1] ==> Patient(s) List
@api_view(['GET','POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def patients_list(request):
    if request.method == "GET":
        users = Profile.objects.all()
        serializers = ProfileSerializer(users, many=True)
        return Response(serializers.data)
    
    elif request.method == "POST":
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# [2.1] ==> Specific User Details 
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def patient_details(request, user_id):
    try:
        # Fetch the profile based on the user_id
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Serialize and return the profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the profile information
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete the profile
        profile.delete()
        return Response({"message": "Profile deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

############################################################## [3] Doctors ##############################################################
# [3.1] ==> Doctor(s) List 
@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def doctors_list(request):
    
    if request.method == 'GET':
        doctors = DoctorsProfileInfo.objects.all()
        serializer = DoctorInfoSerializer(doctors, many=True)
        return Response(serializer.data)
    
# [3.1] ==>  Specific Doctor Details 
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def doctor_details(request, user_id):
    try:
        # Fetch the doctor profile based on the user_id
        doctor = DoctorsProfileInfo.objects.get(user_id=user_id)
    except DoctorsProfileInfo.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Serialize and return the doctor's information
        serializer = DoctorInfoSerializer(doctor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the doctor's information
        serializer = DoctorInfoSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # Delete the doctor's profile
        doctor.delete()
        return Response({"message": "Doctor profile deleted successfully!"})
    
############################################################## [4] Appointments ##############################################################
# [4.1] ==>  Appointment(s) List
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

# [4.2] ==> Specific Appointment Details
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def appointment_details(request, doctor_id):
    try:
        # Fetch the appointment based on the patient foreign key
        appointment = Appointment.objects.get(doctor_id=doctor_id)
    except Appointment.DoesNotExist:
        return Response({"error": "Appointment not found for the given patient ID"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        # Retrieve appointment details
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    elif request.method == "PUT":
        # Update the appointment details
        serializer = AppointmentSerializer(appointment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        # Delete the appointment
        appointment.delete()
        return Response({"message": "Appointment deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

############################################################## [5] Doctor Availability ##############################################################
# [5.1] ==>  Doctor Availability(s) List
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def bookings_list(request):
    
    if request.method == 'GET':
        appointment = DoctorAvailability.objects.all()
        serializer = DoctorAvailabilitySerializer(appointment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DoctorAvailabilitySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Booking has been added successfully :) "}, status= status.HTTP_201_CREATED)
        
    return Response({"message": "Something went wrong to delete :( "}, status=status.HTTP_400_BAD_REQUEST)
    
# [5.2] ==>  Specific Doctor Availability Details 
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def booking_details(request, doctor_id):
    try:
        # Fetch all Activity Feeds associated with the given doctor
        booking = DoctorAvailability.objects.filter(doctor_id=doctor_id)
        if not booking.exists():
            return Response({"error": "No Booking found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid doctor ID"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Retrieve all Activity Feeds for the doctor
        serializer = DoctorAvailabilitySerializer(booking, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        return Response(
            {"error": "Cannot update multiple Bookings(s) at once. Update a specific Booking by its ID."},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        # Delete all Activity Feeds for the doctor
        deleted_count, _ = booking.delete()
        return Response({"message": f"{deleted_count} Bookings(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

########################################################################## [Badr's Views] ##################################################################################################################################

@api_view(['POST'])
def user_login_api_view(request):
    """
    API view to authenticate and log in a user.
    """
    if request.method == 'POST':
        
        serializer = LoginSerializer(data=request.data)

        # Validate the input
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Check if email exists
            if not UserLogin.objects.filter(email=email).exists():
                return Response({'message': 'Email or password does not exist'}, status=status.HTTP_404_NOT_FOUND)

            # Authenticate the user
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)  # Log the user in
                return Response({'message': 'Login successful :)'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid email or password :('}, status=status.HTTP_401_UNAUTHORIZED)

        # Return validation errors
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

####################################################################################################################################################################################################################################################################
# Previous History(s) List
@api_view(['GET', 'POST'])
def previous_history_api_view(request):
    if request.method == 'GET':
        # Retrieve all histories and serialize them
        histories = PreviousHistory.objects.all().order_by('id')
        serializer = PreviousHistorySerializer(histories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new PreviousHistory instance from the request data
        serializer = PreviousHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Previous History Details
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def previous_history_api_view_details(request, sender_id):
    try:
        # Fetch all Previous History associated with the given doctor
        previous = PreviousHistory.objects.filter(sender_id=sender_id)
        if not previous.exists():
            return Response({"error": "No Previous History found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid doctor ID"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Retrieve all Activity Feeds for the doctor
        serializer = PreviousHistorySerializer(previous, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        return Response(
            {"error": "Cannot update multiple Previous History(s) at once. Update a specific Booking by its ID."},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        # Delete all Previous History(s) for the doctor
        deleted_count, _ = previous.delete()
        return Response({"message": f"{deleted_count} Bookings(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
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
    
#####################################################################################################################################################################################################################################

class AlarmAPIView(APIView):
    def get(self, request):
        alarms = Alarm.objects.all()
        serializer = AlarmSerializer(alarms, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id  # Automatically associate the alarm with the logged-in user
        serializer = AlarmSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)