from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "phone_number")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, data):
        user = User.objects.create_user(**data)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)                
                if not user.check_password(password):
                    raise serializers.ValidationError("Invalid credentials")
            except User.DoesNotExist:
                raise serializers.ValidationError("Invalid email")
        else:
            raise serializers.ValidationError("Email and password required")
        
        data["user"] = user
        return data

    
    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "phone_number")
        extra_kwargs = {"password": {"write_only": True}}    