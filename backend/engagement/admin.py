from django.contrib import admin

from models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'created_at')

admin.site.register(Project, ProjectAdmin)