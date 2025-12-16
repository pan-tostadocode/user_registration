#Importamos la funcion 'path' para definir las rutas en Django
from django.urls import path

#Importamos views de la misma app
from . import views

#Importamos directamente la 'view' register
from .views import register

urlpatterns = [
    path('register/', views.register, name='register'), # type: ignore
    path('login/', views.login, name="login"), # type: ignore
    path('logout/', views.logout, name="logout"), # type: ignore
]

#Views --> Funciones o clases que procesan las solicitudes HHTP de los usuarios y devuelven una respuesta HHTP, que puede ser una pagina HTML, JSON, redireccion, etc. 