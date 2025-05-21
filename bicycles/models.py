from django.contrib.gis.db import models


class Bicycle(models.Model):
     bicycle_id = models.AutoField(primary_key=True)
     model = models.CharField(max_length=128)
     coordinates = models.PointField()
     is_rented = models.BooleanField(default=False)
