from django.db import models
from jsonfield import JSONField

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    variations = JSONField(blank=True)

    def __unicode__(self):
        return self.name


class Risk(models.Model):
    name = models.CharField(max_length=100)
    search_string = models.TextField(blank=True)  # search keywords related to this risk
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


