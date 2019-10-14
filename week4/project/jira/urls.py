from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import RegisterUserAPIView, ProjectListAPIView, ProjectDetailAPIVeiw, ProjectMemberViewSet, Task_List, TaskListDetail, TaskCommentAPIView, TaskDocumentViewSet


urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', RegisterUserAPIView.as_view()),
    path('projects/', ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIVeiw.as_view()),
    path('mytasks/', Task_List.as_view()),
    path('projects/<int:pk>/tasks/', TaskListDetail.as_view()),
    path('tasks/<int:pk>/comments/', TaskCommentAPIView.as_view())
]

router = DefaultRouter()
router.register('projects/<int:pk>/members', ProjectMemberViewSet, base_name='projects')
router.register('tasks/<int:pk>/documents', TaskDocumentViewSet, base_name='documents')

urlpatterns += router.urls
