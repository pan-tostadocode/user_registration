# user_registration
Coding Challenge: Simple User Registration y Login con Python/Django y PostgreSQL. Desarrollo en rama "dev", versión final en "main". Frontend con HTML/CSS/JS.


Sistema de registro simple, login y logout de usuarios construido con Django.  
Incluye gestión de sesiones, hashing de contraseñas, bloqueo de usuarios tras intentos fallidos y validaciones de seguridad.

---

## **Características**

- Registro de usuarios con validación de email, contraseña y nombre completo.
- Login seguro con hash de contraseña y control de intentos fallidos.
- Logout que elimina sesiones activas.
- Bloqueo temporal de usuarios tras 3 intentos fallidos (2 horas).
- Backend probado y funcional.
- Comentarios en el código para facilitar mantenimiento.

---

## **Instalación**

1. Clonar el repositorio:
`bash
git clone https://github.com/tu_usuario/user_registration.git
cd user_registration


2. Crear y activar entorno virtual 
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows


3. Instalar dependencias
pip install -r requirements.txt


4. Migrar base de datos
python manage.py migrate


6. Ejecutar servidor
python manage.py runserver


*NOTAS*
> Esta es la versión estable y probada del sistema.
> Código comentado para facilitar mantenimiento y futuras mejoras.
> No incluye estilos ni frontend avanzado (solo funcionalidad backend y JS básico).


---
bytostacode
