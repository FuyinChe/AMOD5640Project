# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customer
from .models import EnvironmentalData


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data.get('username') or email.split('@')[0]
        password = validated_data['password']

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )
        # Create Customer profile linked to this user
        customer = Customer.objects.create(user=user)
        customer.set_verification_code()

        return user


class EnvironmentalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalData
        fields = '__all__'


class MonthlySummarySerializer(serializers.Serializer):
    """Serializer for monthly summarized environmental data"""
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    month_name = serializers.CharField()
    record_count = serializers.IntegerField()
    
    # Air Temperature statistics
    air_temperature_max = serializers.FloatField(allow_null=True)
    air_temperature_min = serializers.FloatField(allow_null=True)
    air_temperature_mean = serializers.FloatField(allow_null=True)
    air_temperature_std = serializers.FloatField(allow_null=True)
    
    # Relative Humidity statistics
    relative_humidity_max = serializers.FloatField(allow_null=True)
    relative_humidity_min = serializers.FloatField(allow_null=True)
    relative_humidity_mean = serializers.FloatField(allow_null=True)
    relative_humidity_std = serializers.FloatField(allow_null=True)
    
    # Shortwave Radiation statistics
    shortwave_radiation_max = serializers.FloatField(allow_null=True)
    shortwave_radiation_min = serializers.FloatField(allow_null=True)
    shortwave_radiation_mean = serializers.FloatField(allow_null=True)
    shortwave_radiation_std = serializers.FloatField(allow_null=True)
    
    # Rainfall statistics
    rainfall_total = serializers.FloatField(allow_null=True)
    rainfall_max = serializers.FloatField(allow_null=True)
    rainfall_mean = serializers.FloatField(allow_null=True)
    rainfall_std = serializers.FloatField(allow_null=True)
    
    # Soil Temperature statistics (5cm)
    soil_temp_5cm_max = serializers.FloatField(allow_null=True)
    soil_temp_5cm_min = serializers.FloatField(allow_null=True)
    soil_temp_5cm_mean = serializers.FloatField(allow_null=True)
    soil_temp_5cm_std = serializers.FloatField(allow_null=True)
    
    # Wind Speed statistics
    wind_speed_max = serializers.FloatField(allow_null=True)
    wind_speed_min = serializers.FloatField(allow_null=True)
    wind_speed_mean = serializers.FloatField(allow_null=True)
    wind_speed_std = serializers.FloatField(allow_null=True)
    
    # Snow Depth statistics
    snow_depth_max = serializers.FloatField(allow_null=True)
    snow_depth_min = serializers.FloatField(allow_null=True)
    snow_depth_mean = serializers.FloatField(allow_null=True)
    snow_depth_std = serializers.FloatField(allow_null=True)
    
    # Atmospheric Pressure statistics
    atmospheric_pressure_max = serializers.FloatField(allow_null=True)
    atmospheric_pressure_min = serializers.FloatField(allow_null=True)
    atmospheric_pressure_mean = serializers.FloatField(allow_null=True)
    atmospheric_pressure_std = serializers.FloatField(allow_null=True)