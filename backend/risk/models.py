from django.db import models
from jsonfield import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Risk(models.Model):
    name = models.CharField(max_length=100)
    search_string = models.TextField(blank=True)  # search keywords related to this risk
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Company(models.Model):
    project = models.ForeignKey('engagement.Project')

    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    variations = JSONField(blank=True)

    risks = models.ManyToManyField(Risk, through='RiskItem', through_fields=('from_company', 'risk'))

    def __unicode__(self):
        return self.name


class RiskItem(models.Model):
    #RiskItem(content_type=article, risk=r)

    risk = models.ForeignKey(Risk)
    project = models.ForeignKey('engagement.Project')
    from_company = models.ForeignKey(Company, related_name='from_company')
    to_company = models.ForeignKey(Company, related_name='to_company', null=True)
    # article = models.ForeignKey('google.SearchResult', related_name='article')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%s : %s : %s" % (self.risk.name, self.from_company.name, self.project.client)

