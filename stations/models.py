from django.contrib.gis.db import models


class EnciclaStation(models.Model):
    station_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    zone = models.CharField(max_length=100, null=True, blank=True)
    geom = models.PointField()

    class Meta:
        # La tabla ya existe, por lo que Django no la gestionará
        managed = False
        db_table = 'encicla_stations'


class EnciclaStationSchema(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
