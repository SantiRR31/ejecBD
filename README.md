# MariaDB Manager Pro 🚀

**MariaDB Manager Pro** es una solución de escritorio moderna, robusta y elegante diseñada para la administración integral de servidores MariaDB. Construida con un enfoque en la experiencia del usuario (UX) y la seguridad de datos, esta herramienta permite gestionar bases de datos, usuarios y respaldos de manera visual y eficiente.

---

## ✨ Características Principales

### 🔒 Sistema de Acceso y Roles (RBAC)
El programa cuenta con un sistema de autenticación de doble capa independiente del motor de base de datos:
- **Login Pro:** Acceso restringido al panel mediante usuarios internos (almacenados en SQLite).
- **Roles Diferenciados:** 
  - **Administrador:** Control total del sistema, gestión de usuarios, creación/eliminación de tablas y respaldos completos.
  - **Usuario (Operador):** Acceso solo-lectura y exploración. No puede eliminar tablas ni gestionar otros usuarios.

### 📊 Explorador de Datos Maestro
- **Visualización de Esquema:** Consulta el DDL (`SHOW CREATE TABLE`) de cualquier tabla con un solo clic.
- **Métricas en Vivo:** Conteo de registros y estadísticas básicas de almacenamiento.
- **Constructor Visual de Tablas:** Crea nuevas tablas sin escribir una sola línea de SQL mediante un formulario dinámico e intuitivo.

### ⌨️ Consola SQL Avanzada
- Ejecución de consultas personalizadas con resaltado de sintaxis (lógica de frontend).
- Tabla de resultados interactiva con soporte para miles de filas.
- Protección contra comandos destructivos para usuarios con roles restringidos.

### 📥 Herramientas de Datos (IO)
- **Importación/Exportación Multiformato:** Soporte completo para **SQL, CSV y JSON**.
- **Respaldo Automático:** Generación de dumps completos del servidor con un solo botón.
- **Inyección de Datos:** Carga masiva de información a tablas existentes o nuevas.

### 🛡️ Auditoría y Seguridad
- **Registros de Actividad:** Historial detallado de cada operación realizada en el sistema (quién, qué, cuándo y cuánto tardó).
- **Backup Scheduler:** Servicio en segundo plano que permite programar respaldos diarios automáticamente.

---

## 🛠️ Tecnologías Utilizadas

- **Frontend/UI:** [Flet](https://flet.dev/) (Basado en Flutter) para una interfaz de escritorio fluida y moderna.
- **Backend:** Python con **SQLAlchemy** para una comunicación robusta con MariaDB.
- **Seguridad:** **Bcrypt** para el cifrado de contraseñas de la aplicación.
- **Datos:** **Pandas** para el manejo eficiente de CSV y JSON.
- **Base de Datos Interna:** SQLite (para control de usuarios y logs).

---

## 🚀 Instalación y Uso

### Requisitos Previos
1. Tener instalado **Python 3.10** o superior.
2. Servidor de **MariaDB/MySQL** activo y accesible.

### Pasos de Instalación
1. Clona o descarga este repositorio.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

### 🔑 Credenciales por Defecto
Al iniciar por primera vez, el sistema crea un administrador maestro:
- **Usuario:** `admin`
- **Contraseña:** `admin123`

---

## 📁 Estructura del Proyecto

```text
├── main.py              # Punto de entrada de la aplicación
├── manager.db           # DB SQLite interna (Usuarios de la App)
├── requirements.txt     # Dependencias de Python
├── db/
│   └── database.py      # Motor de comunicación con MariaDB
├── services/
│   ├── auth_service.py  # Lógica de seguridad y roles
│   ├── monitor_service.py # Sistema de logs y auditoría
│   └── backup_service.py  # Gestión de respaldos y scheduler
├── ui/
│   ├── login_view.py    # Diseño de la pantalla de acceso
│   └── dashboard_view.py # Interfaz principal de administración
└── logs/
    └── monitor.db       # Historial de actividad de usuarios
```

---

## 🎨 Diseño Visual
La aplicación utiliza una estética **Glassmorphism Dark Pro** con acentos en colores Neón (Cian y Púrpura), diseñada para reducir la fatiga visual durante largas horas de administración de datos.

---
*Desarrollado como una solución integral para la gestión ágil de bases de datos.*
