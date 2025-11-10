# Sistema de Gestión Escolar (Flask)

Aplicación web en Python (Flask) para gestionar estudiantes, cursos, profesores y calificaciones, con roles de usuario (admin, docente, estudiante). Usa SQLite por defecto y permite operaciones CRUD básicas y consultas/filtrado.

## Requisitos
- Python 3.x
- Dependencias en `requirements.txt`

## Instalación
1. Crear entorno virtual (Windows):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

2. Variables de entorno: copiar `.env.example` a `.env` y ajustar si es necesario.

3. Ejecutar la aplicación:
   ```powershell
   .\.venv\Scripts\python.exe run.py
   ```
   La aplicación correrá en `http://127.0.0.1:5000/`.

## Roles
- admin: gestiona usuarios (por ahora vía admin inicial), estudiantes, cursos, profesores.
- docente: puede consultar y registrar calificaciones.
- estudiante: puede consultar información y sus calificaciones.

## Módulos
- Gestión: estudiantes, cursos, profesores (CRUD).
- Visualización y consulta: listado con filtros/búsqueda; reportes básicos de calificaciones.

## Base de Datos
- Por defecto: SQLite con archivo `school.db`.
- Configurable mediante `DATABASE_URL` en `.env` (MySQL/PostgreSQL/SQLite).

## Admin por defecto
Al primer arranque, si no existe, se crea automáticamente el usuario admin:
- usuario: `admin`
- contraseña: `admin123`

Se recomienda cambiar la contraseña en producción.

## Estructura
```
app/
  __init__.py
  config.py
  models.py
  auth/
  students/
  courses/
  teachers/
  grades/
  reports/
  templates/
  static/
run.py
requirements.txt
.env.example
README.md
```

## Uso básico
- Iniciar sesión con el admin.
- Crear profesores, estudiantes y cursos.
- Registrar calificaciones vinculando estudiante-curso-profesor.
- Usar filtros de búsqueda en listados y reportes.

## Git
Subir la carpeta del proyecto al repositorio. Incluye `README.md`, `requirements.txt` y `.env.example`. No subir `.env` con secretos reales.