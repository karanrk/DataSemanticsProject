# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db import models
from geoposition.fields import GeopositionField


# Create your models here.

class MyPost(models.Model):
	disease = models.CharField(max_length=500)
	ShowSymptom = models.BooleanField(default=False)
	NearestPrimaryDoctor = models.BooleanField(default=False)
	NearestSecondaryDoctor= models.BooleanField(default=False)
	EstimatedCost = models.BooleanField(default=False)
	user = models.ForeignKey(User)



class PointOfInterest(models.Model):
    name = models.CharField(max_length=100)
    position = GeopositionField()
