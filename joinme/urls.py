from django.urls import path
from . import views
from .views import register

urlpatterns = [
    path('register/', views.register, name='register'), # type: ignore
    path('login/', views.login, name="login"), # type: ignore
    path('logout/', views.logout, name="logout"), # type: ignore
]
