from rest_framework import serializers
from .models import *


class UserserializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class VendorserializerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = UserserializerSerializer()

    class Meta:
        model = Order
        fields = '__all__'
        depth = 1


class DelayReportSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    assigned_to =  UserserializerSerializer()
    class Meta:
        model = DelayReport
        fields = '__all__'
        depth = 1


class CreateDelayReportSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(required=True)
