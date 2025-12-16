#Importamos la librería para generar identificadores únicos (UUID)
import uuid

#Importamos las herramientas para definir modelos(clases o estructura) de la base de datos en Django
from django.db import models

#Importamos funciones para encriptar contraseñas (make_password) y verificarlas (check_password)
from django.contrib.auth.hashers import make_password, check_password

#Definimos modelo que se convertira en una tabla de DB
class User(models.Model): 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=256)
    is_blocked = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password): #Metodo de encriptacion y guardado
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password): #Verificacion
        return check_password(raw_password, self.password)

    def __str__(self): #Represetancion del objeto en texto e email
        return self.email


