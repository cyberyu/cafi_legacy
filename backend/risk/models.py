from django.db import models 

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    zipcode = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Risk(models.Model):
    name = models.CharField(max_length=100)
    search_string = models.TextField(blank=True)  # search keywords related to this risk
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


