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
