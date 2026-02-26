from rest_framework import serializers
from rest_framework import status
from .models import User

class RegisterEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)

    def validate(self, data):
        email = data.get("email")
        
        if not email:
            raise serializers.ValidationError('credentials not provided', status.HTTP_400_BAD_REQUEST)

        return data
    
    def create(self, validate_data):
        email = validate_data.get("email")
        user = User.objects.create_user(email=email)
        return user


class RegisterPhoenNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=False)
    
    def validate(self, data):
        phone_number = data.get("phone_number")
    
        if not phone_number:
            raise serializers.ValidationError('credentials not provided', status.HTTP_400_BAD_REQUEST)
        
        return data
    
    def create(self, validate_data):
        phone_number = validate_data.get("phone_number")
        user = User.objects.create_user(phone_number=phone_number)
        return user


class ActiveUserSerializer(serializers.Serializer):
    verification_code = serializers.CharField()


class ActiveEmailSerializer(ActiveUserSerializer):
    email = serializers.EmailField()
    
    def validate(self, data):
        email = data.get("email")
        
        if not email:
            raise serializers.ValidationError('credentials not provided', status.HTTP_400_BAD_REQUEST)

        return data
    
    def create(self, validated_data):
        email = validated_data.get("email")
        verification_code = validated_data.get("verification_code")
        try:
            user = User.objects.get(email=email).active_user(verification_code=verification_code)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("unexpected error happened.")


class ActivePhoneNumberSerializer(ActiveUserSerializer):
    phone_number = serializers.CharField()
    
    def validate(self, data):
        phone_number = data.get("phone_number")
        
        if not phone_number:
            raise serializers.ValidationError('credentials not provided', status.HTTP_400_BAD_REQUEST)
        return data
    
    
    def create(self, validated_data):
        phone_number = validated_data.get("phone_number")
        verification_code = validated_data.get("verification_code")
        try:
            user = User.objects.get(phone_number=phone_number).active_user(verification_code=verification_code)
            return user
        except User.DoesNotExist:
            raise serializers.ValidationError("unexpected error happened.")