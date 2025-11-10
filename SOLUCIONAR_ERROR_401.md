# Solucionar Error 401 - No se pudieron validar las credenciales

## Problema
El backend rechaza los tokens con error 401 porque la `SECRET_KEY` no está configurada correctamente.

## Solución

### Paso 1: Detener el backend
- Si el backend está corriendo, presiona **Ctrl+C** en la terminal donde está ejecutándose

### Paso 2: Limpiar la base de datos (IMPORTANTE)
Abre CMD o PowerShell en `c:\Users\debr2\Econoconnect\backend` y ejecuta:

```cmd
del test.db
```

Esto elimina la base de datos anterior que tenía tokens inválidos.

### Paso 3: Verificar que existe el archivo .env
El archivo `c:\Users\debr2\Econoconnect\backend\.env` debe existir con este contenido:

```
SECRET_KEY=econoconnect_super_secret_key_2024_production
DATABASE_URL=sqlite:///./test.db
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

Si no existe, créalo manualmente.

### Paso 4: Reiniciar el backend
En la terminal (en `c:\Users\debr2\Econoconnect\backend`), ejecuta:

```cmd
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Paso 5: Limpiar localStorage en el navegador
1. Abre DevTools (F12)
2. Ve a **Application** → **Local Storage**
3. Haz clic en `http://127.0.0.1:5173` (o tu URL del frontend)
4. Elimina todas las entradas (especialmente `token`)
5. Cierra DevTools

### Paso 6: Recarga la página
- Presiona **Ctrl+Shift+R** (recarga completa sin caché)
- O abre una ventana de incógnito

### Paso 7: Vuelve a iniciar sesión
- Usa tus credenciales de usuario
- Deberías ver en la consola:
  - "Token en localStorage: SÍ existe"
  - "¿Comienza con 'eyJ'?: true"
  - "Response status: 200" (NO 401)
  - "✓ Rol data recibido"
  - "✓ Rol normalizado: administrador" (o "usuario")

## Si aún no funciona

1. Verifica que el backend esté corriendo (abre http://127.0.0.1:8000/docs en el navegador)
2. Comparte los logs exactos de la consola del navegador (F12 → Console)
3. Comparte los logs del backend (la terminal donde corre uvicorn)

## Notas importantes
- El archivo `.env` debe estar en `c:\Users\debr2\Econoconnect\backend\.env`
- La `SECRET_KEY` debe ser la misma para crear y validar tokens
- Después de cambiar `.env`, SIEMPRE reinicia el backend
- Después de reiniciar el backend, SIEMPRE limpia localStorage y recarga la página
