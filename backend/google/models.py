from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from engagement.models import Project


class Search(models.Model):
    project = models.ForeignKey(Project, related_name="searches") 
    string = models.CharField(max_length=255) # search string
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
      return self.string


class SearchResult(models.Model):
    search = models.ForeignKey(Search, related_name="results")
    title = models.CharField(max_length=255)
    url = models.URLField(blank=False)
    snippet = models.TextField(blank=True)

    text = models.TextField(blank=True)
    doc_type = models.CharField(blank=True, max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
       return self.title

