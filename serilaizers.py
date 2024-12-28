from rest_framework import serializers
from . models import User, Profile, DoctorsProfileInfo, Appointment, DoctorAvailability, ActivityFeed, PreviousHistory, UserLogin, UploadedPhoto



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
########################################################################################################################################################################

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        
########################################################################################################################################################################

class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorsProfileInfo
        fields = "__all__"
        
################################################################################################################################################################

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        # The clean method in the model ensures validation
        return Appointment.objects.create(**validated_data)
        
################################################################################################################################################################

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
        
################################################################################################################################################################

class ActivityFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityFeed
        fields = '__all__'
        
################################################################################################################################################################        

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'

###############################################################################

class PreviousHistorySerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    class Meta:
        model = PreviousHistory
        fields = ['id', 'sender', 'sender_name', 'message', 'timestamp']
    def get_sender_name(self, obj):
        if obj.sender:
            return obj.sender.name  
        return "Anonymous"

###############################################################################

class UploadedPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPhoto
        fields = ['id', 'uploader', 'photo', 'timestamp']