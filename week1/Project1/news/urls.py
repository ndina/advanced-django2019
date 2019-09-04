from django.urls import path, re_path
from news import views
urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('stuff/', views.Stuff_List.as_view()),
    path('stuff/<int:pk>/', views.StuffStockDetails.as_view()),
]