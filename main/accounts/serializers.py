from rest_framework import serializers
from .models import *
import re

# Import your models here
# from .models import YourModel

class UserSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    created_at = serializers.CharField()  
   
    
# Add more serializers as needed

class UserRegisterSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("شماره تلفن نامعتبر است.")
        return value
    

class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()
    def validate_phone_number(self, value):
        if not re.match(r'^09\d{9}$', value):
            raise serializers.ValidationError("شماره تلفن نامعتبر است.")
        return value

    def validate_code(self, value):
        if not re.match(r'^\d{5}$', value):
            raise serializers.ValidationError("کد OTP باید 5 رقم باشد.")
        return value