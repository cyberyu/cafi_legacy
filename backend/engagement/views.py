from django.shortcuts import render
from django.shortcuts import render, render_to_response

from rest_framework import viewsets

from models import Project
from serializers import ProjectSerializer


def home(request):
	return render_to_response('project_list.html')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer	