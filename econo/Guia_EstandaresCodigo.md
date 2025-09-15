# 📏 Guía de Estándares de Código – EconoConnect

Esta guía define las reglas y convenciones que se deben seguir en el proyecto **EconoConnect**, basado en **Python (FastAPI)** para backend y **JavaScript (React)** para frontend.

---

## 1️⃣ Reglas de Nombres

### Python (FastAPI)
- **Variables** → `snake_case`  
  ✅ `user_name`  
  ❌ `UserName`  
- **Funciones/Métodos** → `snake_case`  
  ✅ `get_user_data()`  
  ❌ `GetUserData()`  
- **Clases** → `PascalCase`  
  ✅ `UserModel`  
  ❌ `user_model`  
- **Constantes** → `UPPER_CASE`  
  ✅ `MAX_RETRIES`  
  ❌ `maxRetries`

### JavaScript (React)
- **Variables y funciones** → `camelCase`  
  ✅ `userName`  
  ❌ `user_name`  
- **Componentes React** → `PascalCase`  
  ✅ `UserProfile`  
  ❌ `userprofile`  
- **Constantes globales** → `UPPER_CASE`  
  ✅ `API_BASE_URL`  
  ❌ `apiBaseUrl`

---

## 2️⃣ Comentarios y Documentación Interna

- **Python** → Usar docstrings triple comillas `"""` para funciones, clases y módulos.  
  ```python
  def get_user(id: int) -> User:
      """
      Obtiene un usuario por su ID.

      Args:
          id (int): Identificador del usuario.

      Returns:
          User: Objeto usuario encontrado.
      """
      ...
