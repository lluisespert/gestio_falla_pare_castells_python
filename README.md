# Gestió Falla Pare Castells

Sistema de gestión integral para la Falla Pare Castells, desarrollado con React (frontend) y Python Flask (backend).

## 🚀 Descripción

Aplicación web completa para la gestión de fallers y pagaments de la Falla Pare Castells. Permite:

- ✅ Gestión completa de fallers (alta, edición, listado, eliminación)
- 💰 Gestión de pagaments con cálculo automático de tarifas
- 📊 Estadísticas y reportes (percentatges, total quotes)
- 📄 Generación de PDFs (listados, recibos)
- 🎯 Cálculo automático de cuotas según edad y grupo

## 🏗️ Arquitectura

### Frontend (React + Vite)
- **Framework:** React 19
- **Build Tool:** Vite
- **Routing:** React Router DOM
- **UI:** Bootstrap 5
- **PDF:** jsPDF + jsPDF-AutoTable

### Backend (Python Flask)
- **Framework:** Flask 3.0
- **Base de datos:** MySQL/MariaDB
- **ORM:** PyMySQL (queries directas)
- **CORS:** Flask-CORS

## 📋 Requisitos

- Node.js 18+ y npm
- Python 3.8+
- MySQL 5.7+ o MariaDB
- XAMPP (opcional, solo si usas MySQL de XAMPP)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd gestio_falla_pare_castells_python
```

### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de MySQL
```

### 3. Configurar Frontend

```bash
# Desde la raíz del proyecto
npm install

# Configurar variables de entorno
copy .env.example .env
# Por defecto apunta a http://localhost:5000/api
```

### 4. Configurar Base de Datos

```bash
# Importar el schema de la base de datos
mysql -u root -p < bbdd/bbdd.sql
```

## ▶️ Ejecución

### Ejecutar Backend (Python Flask)

```bash
cd backend
python app.py
```

El backend estará disponible en `http://localhost:5000`

### Ejecutar Frontend (React + Vite)

```bash
# Desde la raíz del proyecto
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

## 📁 Estructura del Proyecto

```
gestio_falla_pare_castells_python/
├── backend/                    # Backend Python Flask
│   ├── app.py                 # Aplicación principal
│   ├── config.py              # Configuración
│   ├── models/                # Modelos de datos
│   ├── routes/                # Rutas/Endpoints API
│   ├── utils/                 # Utilidades (cálculo tarifas)
│   └── requirements.txt       # Dependencias Python
├── src/                       # Frontend React
│   ├── aplicacion/            # App principal
│   ├── components/            # Componentes reutilizables
│   ├── config/                # Configuración API
│   ├── pages/                 # Páginas/Vistas
│   ├── estilos/               # CSS
│   └── renders/               # Entry point
├── bbdd/                      # Scripts SQL
├── public/                    # Archivos estáticos
└── MIGRATION_GUIDE.md        # Guía de migración PHP → Python
```

## 🔄 Migración de PHP a Python

Este proyecto fue migrado desde un backend PHP a Python Flask. Los archivos PHP originales se mantienen en `src/controller/` pero ya no se usan.

**Mapeo de endpoints:**

| Funcionalidad | PHP (Antiguo) | Python Flask (Nuevo) |
|---------------|---------------|----------------------|
| Listar fallers | `llista_fallers.php` | `GET /api/fallers` |
| Obtener faller | `obtenir_faller.php` | `GET /api/fallers/{id}` |
| Crear faller | `insertar_fallers.php` | `POST /api/fallers` |
| Modificar faller | `modificar_faller.php` | `POST/PUT /api/fallers/{id}` |
| Listar pagaments | `llista_pagaments.php` | `GET /api/pagaments` |
| Crear pagament | `insertar_pagament.php` | `POST /api/pagaments` |
| Info faller | `info_faller_pagament.php` | `GET /api/pagaments/info/{id}` |
| Percentatge | `percentatge.php` | `GET /api/stats/percentatge` |
| Total quotes | `total_quotes.php` | `GET /api/stats/total-quotes` |

Para más detalles, consulta [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)

## 🌐 Endpoints API

### Health Check
- `GET /api/health` - Verificar estado del servidor

### Fallers
- `GET /api/fallers` - Listar todos los fallers
- `GET /api/fallers/{id}` - Obtener un faller
- `POST /api/fallers` - Crear un faller
- `POST/PUT /api/fallers/{id}` - Actualizar un faller
- `DELETE /api/fallers/{id}` - Eliminar un faller

### Pagaments
- `GET /api/pagaments` - Listar todos los pagaments
- `POST /api/pagaments` - Crear un pagament
- `GET /api/pagaments/info/{id}` - Info de pagament de un faller

### Estadísticas
- `GET /api/stats/percentatge` - Fallers por porcentaje de pago
- `GET /api/stats/total-quotes` - Totales agregados

## 🧪 Testing

### Backend
```bash
cd backend
# Probar endpoint de salud
curl http://localhost:5000/api/health

# Listar fallers
curl http://localhost:5000/api/fallers
```

### Frontend
Abrir en el navegador: `http://localhost:5173`

## 🛠️ Scripts Disponibles

### Frontend
- `npm run dev` - Ejecutar en modo desarrollo
- `npm run build` - Compilar para producción
- `npm run preview` - Preview de la build de producción
- `npm run lint` - Ejecutar linter

### Backend
- `python app.py` - Ejecutar servidor Flask

## ⚙️ Configuración

### Variables de Entorno - Frontend (.env)
```env
VITE_API_URL=http://localhost:5000/api
```

### Variables de Entorno - Backend (backend/.env)
```env
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta
DB_HOST=localhost
DB_USER=root
DB_PASS=
DB_NAME=pare_castells
CORS_ORIGINS=*
```

## 📝 Notas Importantes

1. **Puerto Backend:** Por defecto 5000
2. **Puerto Frontend:** Por defecto 5173 (Vite)
3. **CORS:** Configurado para desarrollo (permite todos los orígenes)
4. **Base de datos:** Asegúrate de que MySQL/MariaDB esté ejecutándose
5. **Python:** Usa Python 3.8 o superior

## 🐛 Solución de Problemas

### Error de conexión al backend
- Verifica que el backend esté ejecutándose en `http://localhost:5000`
- Revisa la configuración en `.env` del frontend

### Error de conexión a la base de datos
- Confirma que MySQL esté ejecutándose
- Verifica las credenciales en `backend/.env`
- Asegúrate de que la base de datos `pare_castells` exista

### Error CORS
- Verifica que Flask-CORS esté instalado
- Revisa la configuración CORS en `backend/app.py`

## 📄 Licencia

Este proyecto es para uso interno de la Falla Pare Castells.

## 👥 Contribuciones

Para contribuciones o reportar problemas, contacta con el equipo de desarrollo.
