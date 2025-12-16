#Nos permite devolver respuestas en formato JSON
from django.http import JsonResponse

#Desactiva la proteccion CSRF para estas views
from django.views.decorators.csrf import csrf_exempt

#Fechas y tiempos
from django.utils import timezone
from datetime import timedelta

#Permite acceder y manejar las sesiones activas
from django.contrib.sessions.models import Session

#Datos Json a objetos python
import json

#Encriptacion
from django.contrib.auth.hashers import make_password

#Importamos User
from .models import User
from joinme.models import User

MAX_FAILED_ATTEMPTS = 3 #Intentos
BLOCK_TIME = timedelta(hours=2) #Bloqueo
SESSION_TIMEOUT = 900  # 15 minutos en segundos

#Registro de usuarios
@csrf_exempt
def register(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body) #analizamos y transformamos en uns estructura de datos
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"},
                status=400
            )
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        if len(password) < 8 or not any(c.isdigit() for c in password):
            return JsonResponse({"error": "Weak password"}, status=400)

        if len(full_name) < 5:
            return JsonResponse({"error": "Full name too short"}, status=400)

        user = User.objects.create(
            email=email,
            full_name=full_name,
            password=make_password(password) # type: ignore CONTRASEÑA 
            )


        return JsonResponse({"message": "Successful registration"})

    return JsonResponse({"error": "Method not allowed"}, status=405)


#Inicio de sesion
@csrf_exempt # type: ignore
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

        #Revisamos si el usuario está bloqueado
        if user.is_blocked:
            if user.last_login_attempt and timezone.now() < user.last_login_attempt + BLOCK_TIME:
                return JsonResponse({"error": "User blocked for 2 hours"}, status=403)
            else:
                user.is_blocked = False
                user.failed_attempts = 0
                user.save()

        #Revisamos contraseña
        if user.check_password(password):
            # Limpiar intentos fallidos
            user.failed_attempts = 0
            user.last_login_attempt = timezone.now()
            user.save()

            #Cerramos sesiones activas del mismo usuario
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            for s in sessions:
                data_session = s.get_decoded()
                if data_session.get('_auth_user_id') == str(user.id):
                    s.delete()

            #Creamos nueva sesión
            request.session['_auth_user_id'] = str(user.id)
            request.session.set_expiry(SESSION_TIMEOUT)

            return JsonResponse({"message": f"Welcome {user.full_name}"})

        else:
            #Pass incorrecta
            user.failed_attempts += 1
            user.last_login_attempt = timezone.now()
            if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
                user.is_blocked = True
            user.save()
            return JsonResponse({"error": "Invalid credentials"}, status=400)


#Cierre de sesion
@csrf_exempt
def logout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    #Verificamos si hay usuario logueado
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return JsonResponse({"error": "No hay sesión activa"}, status=400)

    #Eliminamos sesiones activas del usuario
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for s in sessions:
        data_session = s.get_decoded()
        if data_session.get('_auth_user_id') == str(user_id):
            s.delete()

    #Limpiamos session_key en User (si existe)
    try:
        user = User.objects.get(id=user_id)
        user.session_key = None  # type: ignore
        user.save()
    except User.DoesNotExist:
        pass

    #Eliminamos sesión actual
    request.session.flush()  #eliminamos todas las variables de sesión y cookies

    return JsonResponse({"message": "Cierre de sesión exitoso"})
