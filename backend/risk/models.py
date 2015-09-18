from django.db import models 

class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    zipcode = models.CharField(max_length=20)


class Risk(models.Model):
    name = models.CharField(max_length=100)
    keywords = models.TextField(blank=True)  # search keywords related to this risk
    description = models.TextField(blank=True)



