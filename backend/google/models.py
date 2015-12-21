from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.conf import settings

from engagement.models import Project
from risk.models import RiskItem
from django.contrib.auth.models import User

from google.ner.cafi_netagger import CAFI_NETagger
from jsonfield import JSONField


class Search(models.Model):
    STATUS_CHOICES = (
        (0, ''),
        (1, 'in process'),
        (2, 'done'),
    )

    project = models.ForeignKey(Project, related_name="searches")
    user = models.ForeignKey(User)
    string = models.CharField(max_length=1024) # search string
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    is_relevant = models.BooleanField(default=True)

    last_stop = models.IntegerField(default=0)
    has_more_results = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def incr_last_stop(self):
        self.last_stop+=1
        self.save()

    def __unicode__(self):
      return self.string


class SearchResult(models.Model):
    search = models.ForeignKey(Search, related_name="results")
    title = models.CharField(max_length=255)
    url = models.URLField(blank=False, max_length=300)
    snippet = models.TextField(blank=True)
    rank = models.IntegerField(blank=True, null=True)  # rank of the google search result

    raw_html = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    doc_type = models.CharField(blank=True, max_length=20, default='')
    raw_file = models.FileField(blank=True, null=True, max_length=255)

    nerwords = JSONField(blank=True)

    risks = GenericRelation(RiskItem)

    label = models.CharField(max_length=100, default=0)
    relevance = models.CharField(blank=True, max_length=1, default='')
    review_later = models.BooleanField(blank=True, default=False)

    predicted_relevance = models.CharField(blank=True, max_length=1, null=True)
    predicted_score = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    ifduplicated = models.BinaryField(default=False, null=True)
    duplicatedto = models.IntegerField(null=True)


    class Meta:
        ordering = ('rank',)

    def __unicode__(self):
       return self.title

    def get_nerwords(self):
        nt = CAFI_NETagger()  # intialize the tagger
        nt.get_ne_tags_all(self.text)  # tag the text

        self.nerwords = {
            "person": set(nt.get_ne_tags_PERSON()),
            "org": set(nt.get_ne_tags_ORGANIZATION()),
            "location": set(nt.get_ne_tags_LOCATION())
        }


class GeoSearch(models.Model):
    project = models.ForeignKey(Project, related_name="geosearches")
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=1024) # search string
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    status = models.CharField(blank=True, default='', max_length=4)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
      return self.address

