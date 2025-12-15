from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register), # type: ignore
    path('login/', views.login), # type: ignore
    path('logout/', views.logout, name='logout'),
]
