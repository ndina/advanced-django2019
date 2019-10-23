from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from .views import RegisterUserAPIView, ProductViewSet, ServiceViewSet


urlpatterns = [
    path('login', obtain_jwt_token),
    path('register', RegisterUserAPIView.as_view()),
]

router = DefaultRouter()
router.register('products', ProductViewSet, base_name='product')
router.register('services', ServiceViewSet, base_name='service')

urlpatterns += router.urls