from django.core.files.base import ContentFile
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from api.models import UserProfile, User, Order, Shipping, Payment

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserProfileSerializer(serializers.ModelSerializer):
    """User profile Serializer class"""
    class Meta:
        "set field to serialize"
        model = UserProfile
        fields = ('first_name', 'last_name','gov_id','company')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration Serializer Class"""
    profile = UserProfileSerializer(required=False)

    class Meta:
        "set field to serialize"
        model = User
        fields = ('email', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name'],
            gov_id=profile_data['gov_id'],
            company=profile_data['company'],

        )
        return user

class UserLoginSerializer(serializers.Serializer):
    """User login Serializer Class"""

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }

class OrderSerializer(serializers.ModelSerializer):
    """Order Serializer Class"""
    class Meta:
        """set field to serialize"""
        model = Order
        fields = '__all__'

class ShippingSerializer(serializers.ModelSerializer):
    """Order Shipping Class"""
    class Meta:
        """set field to serialize"""
        model = Shipping
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    """Order Payment Class"""
    class Meta:
        """set field to serialize"""
        model = Payment
        fields = '__all__'
