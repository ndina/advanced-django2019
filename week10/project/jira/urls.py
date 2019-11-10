from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import RegisterUserAPIView, ProjectListAPIView, ProjectDetailAPIView, TaskViewSet, TaskDocumentViewSet, TaskCommentViewSet, MemberProjectViewSet


urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', RegisterUserAPIView.as_view()),
    path('projects/', ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIView.as_view()),
]

router = DefaultRouter()
router.register('tasks', TaskViewSet, base_name='jira')
router.register('members', MemberProjectViewSet, base_name='jira')
router.register('documents', TaskDocumentViewSet, base_name='jira')
router.register('comments', TaskCommentViewSet, base_name='jira')

urlpatterns += router.urls
