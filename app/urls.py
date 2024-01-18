from django.urls import path

from .views import AppViewSet,CustomerViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

router.register("app",AppViewSet,basename='app')
router.register("user", CustomerViewSet, basename='customer')

from knox import views as knox_views
from .views import LoginView,register,task

urlpatterns = [
     path('login/', LoginView.as_view(), name='knox_login'),
     path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('register/',register,name='register'),
     path('task/',task), 
]

urlpatterns+=router.urls