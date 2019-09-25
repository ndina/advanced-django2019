from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from .views import RegisterUserAPIView, ProjectListAPIView, ProjectDetailAPIVeiw, ProjectMemberViewSet


urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', RegisterUserAPIView.as_view()),
    path('projects/', ProjectListAPIView.as_view()),
    path('projects/<int:pk>/', ProjectDetailAPIVeiw.as_view())
]

router = DefaultRouter()
router.register('projects/<int:pk>/members', ProjectMemberViewSet, base_name='projects')

urlpatterns += router.urls
