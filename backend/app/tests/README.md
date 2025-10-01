# Tests para Econoconnect Backend

Este directorio contiene los tests unitarios y de integración para todos los endpoints del proyecto Econoconnect.

## Ubicación

Los tests se encuentran en `backend/app/tests/` para mantener la estructura organizacional del proyecto.

## Estructura de Tests

- `conftest.py` - Configuración común para todos los tests (fixtures, base de datos de prueba)
- `test_auth.py` - Tests para endpoints de autenticación (/register, /login, /forgot-password, /reset-password)
- `test_user.py` - Tests para endpoint de perfil de usuario (/me GET)
- `test_user_update.py` - Tests para endpoint de actualización de usuario (/me PUT)
- `test_paises.py` - Tests para endpoints de países (/paises GET, POST)
- `test_noticias.py` - Tests para endpoints de noticias (GET, POST, PUT, PATCH)
- `test_publicaciones.py` - Tests para endpoint de publicaciones (/publicaciones GET)
- `test_etiquetas.py` - Tests para endpoint de etiquetas (/etiquetas GET)
- `test_graficas.py` - Tests para endpoint de gráficas (/graficas GET)
- `test_chat.py` - Tests para endpoint de chats (/chats/{user_id} GET)
- `test_chat_ws.py` - Tests para funcionalidad WebSocket de chat

## Endpoints Cubiertos

### Autenticación (`/api/v1/auth/`)
- `POST /register` - Registro de usuarios
- `POST /login` - Inicio de sesión
- `POST /forgot-password` - Solicitud de recuperación de contraseña
- `POST /reset-password` - Cambio de contraseña con código

### Usuarios (`/api/v1/users/`)
- `GET /me` - Obtener perfil del usuario actual
- `PUT /me` - Actualizar perfil del usuario actual

### Países (`/api/v1/`)
- `GET /paises` - Obtener lista de países
- `POST /paises` - Crear nuevo país

### Noticias (`/api/v1/`)
- `GET /noticias/usuario/{usuario}` - Obtener noticias de un usuario
- `PUT /noticias/{noticia_id}` - Actualizar noticia
- `PATCH /noticias/{noticia_id}/inactivar` - Inactivar noticia
- `GET /noticias` - Obtener todas las noticias
- `POST /noticias` - Crear nueva noticia

### Publicaciones (`/api/v1/`)
- `GET /publicaciones` - Obtener todas las publicaciones

### Etiquetas (`/api/v1/`)
- `GET /etiquetas` - Obtener todas las etiquetas

### Gráficas (`/api/v1/`)
- `GET /graficas` - Obtener datos para gráficas

### Chat (`/api/v1/`)
- `GET /chats/{user_id}` - Obtener chats de un usuario
- `WebSocket /ws/chat/{chat_id}` - Conexión WebSocket para chat en tiempo real

## Requisitos

Antes de ejecutar los tests, asegúrate de tener instaladas las dependencias:

```bash
pip install pytest
pip install pytest-asyncio
pip install httpx  # Para FastAPI TestClient
```

## Ejecución de Tests

### Ejecutar todos los tests
```bash
cd backend
python -m pytest app/tests/
```

### Ejecutar tests específicos
```bash
# Tests de autenticación
python -m pytest app/tests/test_auth.py

# Tests de usuarios
python -m pytest app/tests/test_user.py

# Tests de países
python -m pytest app/tests/test_paises.py

# Tests de noticias
python -m pytest app/tests/test_noticias.py
```

### Ejecutar tests con verbose output
```bash
python -m pytest app/tests/ -v
```

### Ejecutar tests con cobertura
```bash
pip install pytest-cov
python -m pytest app/tests/ --cov=app
```

### Ejecutar un test específico
```bash
python -m pytest app/tests/test_auth.py::test_register_success -v
```

## Configuración de Base de Datos

Los tests utilizan una base de datos SQLite en memoria (`sqlite:///./test.db`) que se crea y destruye automáticamente para cada test. Esto asegura que los tests sean independientes y no interfieran entre sí.

## Fixtures Disponibles

- `client` - Cliente de prueba de FastAPI para hacer requests HTTP
- `test_db` - Sesión de base de datos de prueba

## Funciones Helper

Cada archivo de test incluye funciones helper para crear datos de prueba:
- `create_test_user()` - Crea un usuario de prueba
- `create_auth_headers()` - Crea headers de autenticación con JWT
- `create_test_data()` - Crea datos de prueba específicos para cada módulo

## Mocking

Los tests incluyen mocking para:
- Envío de emails (en tests de recuperación de contraseña)
- Conexiones WebSocket
- Funciones de tiempo para tests de expiración

## Casos de Prueba Incluidos

### Tests Exitosos
- Registro de usuario válido
- Login con credenciales correctas
- Actualización de perfil
- Creación y obtención de datos

### Tests de Error
- Credenciales inválidas
- Datos duplicados
- Recursos no encontrados
- Tokens inválidos o expirados
- Validación de datos

### Tests de Edge Cases
- Datos vacíos
- Valores límite
- Estados de datos especiales

## Notas Importantes

1. **Base de datos limpia**: Cada test comienza con una base de datos limpia
2. **Independencia**: Los tests no dependen unos de otros
3. **Mocking**: Se utilizan mocks para servicios externos (email, etc.)
4. **Autenticación**: Los tests que requieren autenticación incluyen tokens JWT válidos
5. **WebSocket**: Los tests de WebSocket utilizan mocks debido a la complejidad de testing en tiempo real

## Problemas Conocidos

1. En `chat_ws.py` hay un typo: `get_db` en lugar de `get` en la línea del broadcast
2. Los tests de WebSocket son limitados debido a la complejidad de testing de conexiones en tiempo real
3. Algunos endpoints pueden requerir datos adicionales según la evolución del proyecto

## Contribuir

Al agregar nuevos endpoints:
1. Crea un nuevo archivo `test_<nombre_endpoint>.py`
2. Incluye tests para casos exitosos y de error
3. Utiliza las fixtures y helpers existentes
4. Documenta cualquier setup especial requerido