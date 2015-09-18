from rest_framework import viewsets

from models import Project
from serializers import ProjectSerializer


def home(request):
	return render_to_response('home.html')

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer	