from .models import User, Profile, DoctorsProfileInfo, Appointment, Booking, ActivityFeed, UserLogin, PreviousHistory, UploadedPhoto
from .serilaizers import  UserSerializer, ProfileSerializer, DoctorInfoSerializer, AppointmentSerializer, BookingSerializer, ActivityFeedSerializer, LoginSerializer , PreviousHistorySerializer, UploadedPhotoSerializer

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

########################################################################## {Django REST Framework} #########################################################################################################

################################################################################# [1] Users ###############################################################################################################################################################################################################################################

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def users_list(request):
    user = User.objects.all()
    
    if request.method == 'GET':
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "A new user has been added successfully :) "}, status= status.HTTP_201_CREATED)
        
    return Response({"message": "Something went wrong to delete :( "}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_details(request, pk):
    
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

# [1.1] ==> Specific User Details 
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
def appointment_details(request, patient_id):
    try:
        # Fetch the appointment based on the patient foreign key
        appointment = Appointment.objects.get(patient_id=patient_id)
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

############################################################## [5] Booking ##############################################################
    
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def bookings_list(request):
    
    if request.method == 'GET':
        appointment = Booking.objects.all()
        serializer = BookingSerializer(appointment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = BookingSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Booking has been added successfully :) "}, status= status.HTTP_201_CREATED)
        
    return Response({"message": "Something went wrong to delete :( "}, status=status.HTTP_400_BAD_REQUEST)

# [3.1] ==> Specific Patient Booking
# @api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])
# def bookings_details(request, doctor_id):
#     try:
#         # Fetch the booking based on the doctor foreign key
#         booking = Booking.objects.get(doctor_id=doctor_id)
#     except Booking.DoesNotExist:
#         return Response({"error": "Booking not found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == "GET":
#         # Retrieve booking details
#         serializer = BookingSerializer(booking)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         # Update the booking details
#         serializer = BookingSerializer(booking, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "DELETE":
#         # Delete the booking
#         booking.delete()
#         return Response({"message": "Booking deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def booking_details(request, doctor_id):
    try:
        # Fetch all Activity Feeds associated with the given doctor
        booking = Booking.objects.filter(doctor_id=doctor_id)
        if not booking.exists():
            return Response({"error": "No Booking found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid doctor ID"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Retrieve all Activity Feeds for the doctor
        serializer = BookingSerializer(booking, many=True)
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

############################################################## [6] Activity Feed ##############################################################

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def activity_feeds_list(request):
    
    if request.method == 'GET':
        appointment = ActivityFeed.objects.all()
        serializer = ActivityFeedSerializer(appointment, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ActivityFeedSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Activity Feed has been added successfully :) "}, status= status.HTTP_201_CREATED)
        
    return Response({"message": "Something went wrong to delete :( "}, status=status.HTTP_400_BAD_REQUEST)

# [3.1] ==> Specific Activity Feed
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def activity_feed_details(request, doctor_id):
    try:
        # Fetch all Activity Feeds associated with the given doctor
        activity_feeds = ActivityFeed.objects.filter(doctor_id=doctor_id)
        if not activity_feeds.exists():
            return Response({"error": "No Activity Feeds found for the given doctor ID"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "Invalid doctor ID"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        # Retrieve all Activity Feeds for the doctor
        serializer = ActivityFeedSerializer(activity_feeds, many=True)
        return Response(serializer.data)

    elif request.method == "PUT":
        return Response(
            {"error": "Cannot update multiple Activity Feeds at once. Update a specific Activity Feed by its ID."},
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == "DELETE":
        # Delete all Activity Feeds for the doctor
        deleted_count, _ = activity_feeds.delete()
        return Response({"message": f"{deleted_count} Activity Feed(s) deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)

############################################################################################################################################################################################################

class LoginAPI(APIView):
    def get(self, request):
        users = UserLogin.objects.all()  
        data = [{"name": user.name, "national_id": user.national_id} for user in users]  
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            national_id = serializer.validated_data['national_id']
            try:
                user = UserLogin.objects.get(name=name, national_id=national_id)
                return Response({"message": "Login successful", "redirect": "home"}, status=status.HTTP_200_OK)
            except UserLogin.DoesNotExist:
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