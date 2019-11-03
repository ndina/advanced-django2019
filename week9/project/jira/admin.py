from django.contrib import admin
from .models import Project, UserProfile, ProjectMember, TaskComment, Task, TaskDocument

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(TaskDocument)
admin.site.register(Task)
admin.site.register(TaskComment)


