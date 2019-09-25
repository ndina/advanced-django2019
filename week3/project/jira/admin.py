from django.contrib import admin
from .models import Project, UserProfile, ProjectMember

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(ProjectMember)
