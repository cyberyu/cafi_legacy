from django.db import models
from jsonfield import JSONField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class PredefinedSearch(models.Model):
    name = models.CharField(max_length=100)
    search_string = models.TextField(blank=True) # search keywords related to this risk
    is_global = models.BooleanField(default=True)  # show to all users
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class Risk(models.Model):
    name = models.CharField(max_length=100)
    search_string = models.TextField(blank=True)
    description = models.TextField(blank=True)
    type = models.IntegerField(choices=((1, 'major risk'), (2, 'sub risk')), default=1)
    parent = models.ForeignKey('self', blank=True, null=True, default=None, related_name='subrisks')

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
    risk = models.ForeignKey(Risk, related_name='risk_items')
    # risk_type = models.IntegerField(choices=((1, 'primary'), (2, 'secondary'), (3,'tertiary')))
    subrisk = models.ForeignKey(Risk, related_name='subrisk_items', blank=True, null=True)
    project = models.ForeignKey('engagement.Project')
    from_company = models.ForeignKey(Company, related_name='from_company')
    to_company = models.ForeignKey(Company, related_name='to_company', null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%s : %s : %s" % (self.risk.name, self.from_company.name, self.project.client)


class Relation(models.Model):
    evidence = models.ForeignKey('google.SearchResult')
    buyer = models.ForeignKey(Company, related_name='buyer_company')
    supplier = models.ForeignKey(Company, related_name='supplier_company')
    item_list = models.TextField(blank=True)


