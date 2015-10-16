from django.db import models
from jsonfield import JSONField


class Risk(models.Model):
    name = models.CharField(max_length=100)
    search_string = models.TextField(blank=True)  # search keywords related to this risk
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    variations = JSONField(blank=True)

    risks = models.ManyToManyField(Risk, through='CompanyRisk', through_fields=('from_company', 'risk'))

    def __unicode__(self):
        return self.name


class CompanyRisk(models.Model):
    risk = models.ForeignKey(Risk)
    from_company = models.ForeignKey(Company, related_name='from_company')
    to_company = models.ForeignKey(Company, related_name='to_company')

