Configuración segura
====================

Backend
-------

El backend requiere DJANGO_SECRET_KEY (mínimo 50 caracteres). No guardes este
valor ni las credenciales de base de datos en el repositorio. Configura también:

- DB_USER, DB_PASSWORD, DB_HOST y DB_PORT
- DJANGO_ALLOWED_HOSTS: hosts separados por comas, sin puertos
- DJANGO_CORS_ALLOWED_ORIGINS y DJANGO_CSRF_TRUSTED_ORIGINS: orígenes separados
	por comas e incluyendo el esquema, por ejemplo http://localhost:8080
- DJANGO_DEBUG: usa true solo en desarrollo
- DJANGO_HTTPS_ONLY: por defecto sigue DEBUG; producción debe usar HTTPS
- DJANGO_TRUST_PROXY_SSL_HEADER: true solo si un proxy confiable establece
	X-Forwarded-Proto correctamente

Para crear el superusuario, configura además DJANGO_SUPERUSER_USERNAME,
DJANGO_SUPERUSER_EMAIL y DJANGO_SUPERUSER_PASSWORD antes de ejecutar el comando
create_superusers.

El frontend de producción usa /api en el mismo origen. Configura el proxy web
para dirigir /api y /ws al backend; el WebSocket requiere un JWT vigente.

Rotación de credenciales
------------------------

La clave Django y la contraseña de PostgreSQL que estaban en el código deben
considerarse comprometidas si alguna vez se usaron. Rótalas en sus sistemas,
invalida sesiones/tokens firmados con la clave anterior y revisa el historial
del repositorio y los logs de despliegue. Eliminar un secreto del último commit
no lo elimina de commits anteriores.
