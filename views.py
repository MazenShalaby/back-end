from .models import User, Profile, DoctorsProfileInfo, Booking_Appointments, DoctorAvailability, PreviousHistory, UploadedPhoto, Alarm
from .serilaizers import  (UserSerializer, ProfileSerializer, DoctorInfoSerializer, AppointmentSerializer, DoctorAvailabilitySerializer,
CustomUserLoginSerializer , PreviousHistorySerializer, UploadedPhotoSerializer, AlarmSerializer)

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
    
############################################################## [4] Doctor Availability ##############################################################
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

############################################################## [5] Booking An Appointments ##############################################################
# [4.1] ==>  Appointment(s) List
@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def book_appointments_list(request):
    """
    - GET: Retrieve all appointments.
    - POST: Create a new appointment, ensuring no duplicate bookings for the same doctor, date, and time.
    - DELETE: Delete all appointments.
    """
    if request.method == 'GET':
        appointments = Booking_Appointments.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.validated_data['doctor']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']

            # Check if the appointment slot is already booked by another patient
            if Booking_Appointments.objects.filter(doctor=doctor, date=date, time=time, available=False).exists():
                return Response(
                    {"error": "This appointment slot is already booked by another patient."}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Save the new appointment
            appointment = serializer.save()

            # Ensure the appointment is marked as unavailable
            appointment.available = False
            appointment.save(update_fields=['available'])

            return Response(
                {"message": "An appointment has been booked successfully!", "data": serializer.data}, 
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Delete all appointments
        Booking_Appointments.objects.all().delete()
        return Response({"message": "All appointments have been deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)



# [4.2] ==> Specific Appointment Details
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def book_appointment_details(request, doctor_id):
    try:
        # Fetch the appointment based on the patient foreign key
        appointment = Booking_Appointments.objects.get(doctor_id=doctor_id)
    except Booking_Appointments.DoesNotExist:
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

# ############################################################## [6] Booked Appointments ##############################################################
# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
# def booked_appointements_list(request):
    
#     booked = BookedAppointment.objects.all()
    
#     if request.method == "GET":
#         serializers = BookedAppointmentSerializer(booked, many=True)
#         return Response(serializers.data)
    
# @api_view(['GET', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
# def booked_appointment_details(request, patient_id):
#     try:
#         # Fetch the appointment based on the patient foreign key
#         booked = BookedAppointment.objects.get(patient_id=patient_id)
#     except BookedAppointment.DoesNotExist:
#         return Response({"error": "Appointment not found for the given patient ID"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         # Retrieve appointment details
#         serializer = BookedAppointmentSerializer(booked)
#         return Response(serializer.data)
    
#     elif request.method == "DELETE":
#         # Delete the appointment
#         booked.delete()
#         return Response({"message": "Appointment deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

########################################################################## [Badr's Views] ##################################################################################################################################
########################################################################## [7] Login Api ##################################################################################################################################
# [6] ==> Login API
@api_view(['POST'])
def custom_user_login(request):
    """
    Login API for the custom user model.
    """
    serializer = CustomUserLoginSerializer(data=request.data)
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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