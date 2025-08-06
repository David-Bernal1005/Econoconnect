# 🔄 Flujo de Trabajo con Git – EconoConnect

Este documento describe las convenciones y prácticas para trabajar con **Git** en el proyecto **EconoConnect**.

---

## 1️⃣ Convención de Commits
Usaremos el formato **[Conventional Commits](https://www.conventionalcommits.org/)**:


### Tipos permitidos:
- **feat** → Nueva funcionalidad (ej. `feat(api): agregar endpoint de registro`)
- **fix** → Corrección de errores (ej. `fix(auth): resolver bug en token de sesión`)
- **docs** → Cambios en documentación (ej. `docs(readme): actualizar requisitos previos`)
- **style** → Cambios de formato (sin afectar la lógica) (ej. `style(ui): ajustar indentación en Header`)
- **refactor** → Refactorización de código (ej. `refactor(db): optimizar consultas`)
- **test** → Cambios en pruebas (ej. `test(user): agregar test para login`)
- **chore** → Cambios en tareas y configuraciones (ej. `chore(deps): actualizar dependencias`)

📌 **Reglas:**
- Usar descripciones claras y en **presente**.
- No exceder **72 caracteres** en el título del commit.
- Incluir detalles extra en el cuerpo si es necesario.

---

## 2️⃣ Flujo de Ramas
- **main** → Contiene el código estable y listo para producción.
- **develop** → Rama donde se integran todas las funcionalidades antes de pasarlas a `main`.
- **feature/<nombre>** → Ramas temporales para desarrollar nuevas funcionalidades.

📌 Ejemplo:
```bash
# Crear nueva rama de funcionalidad
git checkout develop
git pull origin develop
git checkout -b feature/login-usuarios


```

## 3️⃣ Frecuencia de Push/Pull
- **Push**: Se deben realizar pushes frecuentes (idealmente después de completar una tarea o al final de la jornada) para evitar pérdida de trabajo.
- **Pull**: Hacer `git pull` antes de iniciar el trabajo diario para sincronizar con la última versión de la rama.
- **Regla**: No trabajar más de un día sin sincronizar cambios con el repositorio remoto.

## 4️⃣ Política de Pull Requests
1. Desde ramas `feature/*` hacia `develop`.
2. Descripción clara de cambios realizados.
3. Al menos 1 aprobación de otro miembro del equipo.
4. Pasar todos los tests antes de mergear.
5. Merge a `main` solo desde `develop` con versión etiquetada (`vX.X.X`).

---

## 5️⃣ Plantilla de Pull Request
### 📝 Descripción
<!-- Explica brevemente qué cambios realizaste y por qué -->

### 🔍 Cambios Realizados
- [ ] Nueva funcionalidad
- [ ] Corrección de bug
- [ ] Actualización de documentación
- [ ] Refactor de código
- [ ] Otro (especificar)

### 📸 Evidencia (opcional)
<!-- Capturas de pantalla, gifs o ejemplos que muestren los cambios -->

### ✅ Checklist
- [ ] El código compila sin errores
- [ ] Los tests pasan correctamente
- [ ] Cumple con los estándares de código
- [ ] Documentación actualizada
