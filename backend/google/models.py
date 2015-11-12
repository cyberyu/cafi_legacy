from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from django.conf import settings

from engagement.models import Project
from risk.models import RiskItem
from django.contrib.auth.models import User


class Search(models.Model):
    STATUS_CHOICES = (
        (0, ''),
        (1, 'submitted'),
        (2, 'in process'),
        (3, 'done'),
    )

    project = models.ForeignKey(Project, related_name="searches")
    string = models.CharField(max_length=1024) # search string
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
      return self.string


class SearchResult(models.Model):
    LABEL_CHOICES = (
        (0, ''),
        (1, 'junk'),
        (2, 'risk'),
        (3, 'biz'),
    )

    search = models.ForeignKey(Search, related_name="results")
    user = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    url = models.URLField(blank=False)
    snippet = models.TextField(blank=True)
    rank = models.IntegerField(blank=True, null=True)  # rank of the google search result

    raw_html = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    doc_type = models.CharField(blank=True, max_length=20)
    raw_file = models.FileField(blank=True, null=True)

    risks = GenericRelation(RiskItem)

    label = models.IntegerField(choices=LABEL_CHOICES, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('rank',)

    def __unicode__(self):
       return self.title


class GeoSearch(models.Model):
    project = models.ForeignKey(Project, related_name="geosearches")
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=1024) # search string
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    status = models.CharField(blank=True, default='', max_length=4)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
    #     unique_together = ('name', 'address')

    def __unicode__(self):
      return self.address


