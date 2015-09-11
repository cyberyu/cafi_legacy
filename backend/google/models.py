from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from engagement.models import Project

# Create your models here.
class Search(models.Model):
    project = models.ForeignKey(Project) 
    string = models.CharField(max_length=255) # search string
    created_at = models.DateTimeField(auto_now_add=True)


class SearchResult(models.Model):
    search = models.ForeignKey(Search)
    title = models.CharField(max_length=255)
    snippet = models.TextField()
    url = models.URLField()

