from rest_framework import serializers
from . models import (User, Profile, DoctorsProfileInfo, Appointment, DoctorAvailability, PreviousHistory, UserLogin, UploadedPhoto, Alarm)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        """
        Hash the password before saving the user instance.
        """
        password = validated_data.pop('password', None)  # Extract the raw password
        user = super().create(validated_data)  # Create the user without the password initially
        if password:
            user.set_password(password)  # Hash the password
            user.save()  # Save the user instance with the hashed password
        return user

    def update(self, instance, validated_data):
        """
        Hash the password if it is updated.
        """
        password = validated_data.pop('password', None)  # Extract the raw password
        instance = super().update(instance, validated_data)  # Update other fields
        if password:
            instance.set_password(password)  # Hash the password
            instance.save()  # Save the user instance with the hashed password
        return instance
        
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
        
######################################################################### [Badr's Serializers] #######################################################################################        

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLogin
        fields = '__all__'

###############################################################################

class PreviousHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreviousHistory
        fields = '__all__'

###############################################################################

class UploadedPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedPhoto
        fields = ['id', 'uploader', 'photo', 'timestamp']
        
###############################################################################

class AlarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alarm
        fields = '__all__'