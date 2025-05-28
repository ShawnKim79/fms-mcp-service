from django.db import models

class Passenger(models.Model):
    name = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)

class Vehicle(models.Model):
    numberPlate = models.CharField(max_length=10)
    ownerPassenger = models.IntegerField()
    maxPassenger = models.SmallIntegerField()

class Trip(models.Model):
    vehicle = models.IntegerField()
    startTime = models.DateTimeField()
    departureLocationLat = models.FloatField()
    departureLocationLng = models.FloatField()
    arrivalLocationLat = models.FloatField()
    arrivalLocationLng = models.FloatField()
    
class Route(models.Model):
    passenger = models.IntegerField()
    onboardTime = models.DateTimeField()
    departureLocationLat = models.FloatField()
    departureLocationLng = models.FloatField()    
    arrivalLocationLat = models.FloatField()
    arrivalLocationLng = models.FloatField()