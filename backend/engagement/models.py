from django.db import models
from risk.models import Company

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255) 
    client = models.CharField(max_length=100)
    companies = models.ManyToManyField(Company, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
       ordering = ('created_at',)

    def __unicode__(self):
        return self.name