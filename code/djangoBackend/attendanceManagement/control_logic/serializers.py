from rest_framework import serializers
from attendanceManagement.models import *


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDetails
        fields = '__all__'


class AttendanceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceDetails
        fields = '__all__'


class PinDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PinData
        fields = '__all__'