from django.contrib.auth.models import User
from django.db import models
from datetime import datetime, timedelta
import random

# generate random verification code
def generate_verification_code():
    return str(random.randint(100000, 999999))

# customize the customers or users
class Customer(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # allow null for migration
    email_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    code_expires_at = models.DateTimeField(blank=True, null=True)

    def set_verification_code(self):
        self.verification_code = generate_verification_code()
        self.code_expires_at = datetime.now() + timedelta(minutes=10)
        self.save()



#define environmental data class
class EnvironmentalData(models.Model):
    id = models.IntegerField(primary_key=True)
    Timestamp = models.CharField(max_length=50)
    DOY = models.FloatField()
    AirTemperature_degC = models.FloatField(null=True, blank=True)
    RelativeHumidity_Pct = models.FloatField(null=True, blank=True)
    ShortwaveRadiation_Wm2 = models.FloatField(null=True, blank=True)
    Rainfall_mm = models.FloatField(null=True, blank=True)
    SoilTemperature_5cm_degC = models.FloatField(null=True, blank=True)
    SoilTemperature_20cm_degC = models.FloatField(null=True, blank=True)
    SoilTemperature_50cm_degC = models.FloatField(null=True, blank=True)
    WindSpeed_ms = models.FloatField(null=True, blank=True)
    WindVector_ms = models.FloatField(null=True, blank=True)
    WindDirection_deg = models.FloatField(null=True, blank=True)
    WindDirectionSD_deg = models.FloatField(null=True, blank=True)
    SnowDepth_m = models.FloatField(null=True, blank=True)
    LoggerTemperature_degC = models.FloatField(null=True, blank=True)
    LoggerVoltage_V = models.FloatField(null=True, blank=True)
    TotalPrecipitation_mV = models.FloatField(null=True, blank=True)
    TotalPrecipitation_mm = models.FloatField(null=True, blank=True)
    AtmosphericPressure_kPa = models.FloatField(null=True, blank=True)
    BatteryVoltage_V = models.FloatField(null=True, blank=True)
    MinutesOut_min = models.FloatField(null=True, blank=True)
    PanelTemp_degC = models.FloatField(null=True, blank=True)
    SnowDepth_cm = models.FloatField(null=True, blank=True)
    SolarRadiation_Wm2 = models.FloatField(null=True, blank=True)
    SoilTemperature_10cm_degC = models.FloatField(null=True, blank=True)
    SoilTemperature_25cm_degC = models.FloatField(null=True, blank=True)
    Record_TCS_30min = models.FloatField(null=True, blank=True)
    LoggerTemp_degC = models.FloatField(null=True, blank=True)
    BarometricPressure_TCS_kPa = models.FloatField(null=True, blank=True)
    Year = models.IntegerField()
    Month = models.IntegerField()
    Day = models.IntegerField()
    Time = models.CharField(max_length=20)

    class Meta:
        managed = False  # because this table already exists in MySQL
        db_table = 'environmental_data'

