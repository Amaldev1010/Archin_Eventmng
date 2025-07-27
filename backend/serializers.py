
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Event, Registration

# Custom user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'department', 'year_of_study', 'college_name']

# Register user serializer (for signup)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'phone_number', 'department', 'year_of_study', 'college_name']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            role=validated_data['role'],
            phone_number=validated_data.get('phone_number', ''),
            department=validated_data.get('department', ''),
            year_of_study=validated_data.get('year_of_study', ''),
            college_name=validated_data.get('college_name', ''),
        )
        return user

# Login serializer (to verify credentials)
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                return {"user": user}
            raise serializers.ValidationError("Invalid username or password.")
        else:
            raise serializers.ValidationError("Both 'username' and 'password' are required.")

# Event serializer
class EventSerializer(serializers.ModelSerializer):
    coordinator = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'location', 'date', 'time', 'coordinator']

# Participant info inside registration
class RegistrationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    phone_number = serializers.CharField(source='user.phone_number')
    department = serializers.CharField(source='user.department')
    year_of_study = serializers.CharField(source='user.year_of_study')
    college_name = serializers.CharField(source='user.college_name')
    event_title = serializers.CharField(source='event.title')

    class Meta:
        model = Registration
        fields = ['id', 'name', 'email', 'phone_number', 'department', 'year_of_study', 'college_name', 'event_title']