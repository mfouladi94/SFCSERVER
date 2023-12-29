from rest_framework import serializers
from .models import *


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class LoginSerializerInput(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(
        min_length=5, max_length=50, required=True)
