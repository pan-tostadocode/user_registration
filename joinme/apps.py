#Importamos la clase AppConfig de Django para configurar una aplicación dentro de un proyecto Django, en este caso 'JoinMe'
from django.apps import AppConfig


class JoinmeConfig(AppConfig): #Definimos una nueva clase llamada JoinmeConfig. Estamos creando la configuración de una app Django
    name = 'joinme' #Indicamos el nombre de la aplicación.

