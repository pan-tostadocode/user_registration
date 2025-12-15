from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
from django.contrib.sessions.models import Session
import json
from django.contrib.auth.hashers import make_password
from .models import User


MAX_FAILED_ATTEMPTS = 3
BLOCK_TIME = timedelta(hours=2)
SESSION_TIMEOUT = 900  # 15 minutos en segundos

from joinme.models import User

@csrf_exempt
def register(request):
    if request.method == "POST":

        try:
            data = json.loads(request.body)
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

        # Revisar si el usuario está bloqueado
        if user.is_blocked:
            if user.last_login_attempt and timezone.now() < user.last_login_attempt + BLOCK_TIME:
                return JsonResponse({"error": "User blocked for 2 hours"}, status=403)
            else:
                user.is_blocked = False
                user.failed_attempts = 0
                user.save()

        # Revisar contraseña
        if user.check_password(password):
            # Limpiar intentos fallidos
            user.failed_attempts = 0
            user.last_login_attempt = timezone.now()
            user.save()

            # Cerrar sesiones activas del mismo usuario
            sessions = Session.objects.filter(expire_date__gte=timezone.now())
            for s in sessions:
                data_session = s.get_decoded()
                if data_session.get('_auth_user_id') == str(user.id):
                    s.delete()

            # Crear nueva sesión
            request.session['_auth_user_id'] = str(user.id)
            request.session.set_expiry(SESSION_TIMEOUT)

            return JsonResponse({"message": f"Welcome {user.full_name}"})

        else:
            # Contraseña incorrecta
            user.failed_attempts += 1
            user.last_login_attempt = timezone.now()
            if user.failed_attempts >= MAX_FAILED_ATTEMPTS:
                user.is_blocked = True
            user.save()
            return JsonResponse({"error": "Invalid credentials"}, status=400)



@csrf_exempt
def logout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    # Verificar si hay usuario logueado
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return JsonResponse({"error": "No hay sesión activa"}, status=400)

    # Eliminar sesiones activas del usuario
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for s in sessions:
        data_session = s.get_decoded()
        if data_session.get('_auth_user_id') == str(user_id):
            s.delete()

    # Limpiar session_key en User (si existe)
    try:
        user = User.objects.get(id=user_id)
        user.session_key = None  # type: ignore
        user.save()
    except User.DoesNotExist:
        pass

    # Eliminar sesión actual
    request.session.flush()  # elimina todas las variables de sesión y cookie

    return JsonResponse({"message": "Cierre de sesión exitoso"})
