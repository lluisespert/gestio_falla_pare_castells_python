# Backend Python - Gestió Falla Pare Castells

Backend desarrollado en Python con Flask para la gestión de la Falla Pare Castells. Este backend reemplaza la implementación original en PHP manteniendo todas las funcionalidades.

## 🚀 Características

- **API RESTful** completa con Flask
- **Gestión de Fallers**: CRUD completo (crear, leer, actualizar, eliminar)
- **Gestión de Pagaments**: Registro y seguimiento de pagos
- **Estadísticas**: Cálculo de porcentajes y totales agregados
- **Cálculo automático de tarifas** según grupo y edad
- **CORS configurado** para integración con frontend React
- **Base de datos MySQL** con PyMySQL

## 📋 Requisitos Previos

- Python 3.8 o superior
- MySQL 5.7 o superior (o MariaDB)
- pip (gestor de paquetes de Python)

## 🔧 Instalación

### 1. Clonar o navegar al directorio del backend

```bash
cd backend
```

### 2. Crear entorno virtual (recomendado)

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiar el archivo `.env.example` a `.env`:

```bash
copy .env.example .env
```

Editar el archivo `.env` con tus credenciales de base de datos:

```env
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui

DB_HOST=localhost
DB_USER=root
DB_PASS=
DB_NAME=pare_castells

CORS_ORIGINS=*
```

### 5. Configurar la base de datos

Asegúrate de que la base de datos MySQL esté creada y configurada. Puedes usar el script SQL en `../bbdd/bbdd.sql`:

```bash
mysql -u root -p < ../bbdd/bbdd.sql
```

## ▶️ Ejecución

### Modo desarrollo

```bash
python app.py
```

El servidor se iniciará en `http://localhost:5000`

### Modo producción (con Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 Endpoints de la API

### Health Check

- **GET** `/api/health` - Verificar estado del servidor

### Fallers

- **GET** `/api/fallers` - Obtener todos los fallers
- **GET** `/api/fallers/<id>` - Obtener un faller por ID
- **POST** `/api/fallers` - Crear un nuevo faller
- **POST/PUT** `/api/fallers/<id>` - Actualizar un faller
- **DELETE** `/api/fallers/<id>` - Eliminar un faller

### Pagaments

- **GET** `/api/pagaments` - Obtener todos los pagaments
- **POST** `/api/pagaments` - Crear un nuevo pagament
- **GET** `/api/pagaments/info/<id_faller>` - Obtener información de pagaments de un faller

### Estadísticas

- **GET** `/api/stats/percentatge` - Obtener fallers agrupados por porcentaje de pago
- **GET** `/api/stats/total-quotes` - Obtener totales agregados

## 📁 Estructura del Proyecto

```
backend/
├── app.py                 # Aplicación principal Flask
├── config.py              # Configuración de la aplicación
├── requirements.txt       # Dependencias Python
├── .env.example          # Plantilla de variables de entorno
├── models/               # Modelos de datos
│   ├── __init__.py
│   ├── database.py       # Gestor de conexiones
│   ├── faller.py         # Modelo Faller
│   ├── pagament.py       # Modelo Pagament
│   └── stats.py          # Modelo Stats
├── routes/               # Rutas/Endpoints
│   ├── __init__.py
│   ├── fallers.py        # Rutas de fallers
│   ├── pagaments.py      # Rutas de pagaments
│   └── stats.py          # Rutas de estadísticas
└── utils/                # Utilidades
    ├── __init__.py
    └── tariffs.py        # Cálculo de tarifas
```

## 🔄 Migración desde PHP

Este backend reemplaza completamente los archivos PHP ubicados en `src/controller/`:

| Archivo PHP | Equivalente Python |
|-------------|-------------------|
| `config.php` | `config.py` + `models/database.py` |
| `insertar_fallers.php` | `routes/fallers.py` (POST /) |
| `llista_fallers.php` | `routes/fallers.py` (GET /) |
| `obtenir_faller.php` | `routes/fallers.py` (GET /<id>) |
| `modificar_faller.php` | `routes/fallers.py` (POST/PUT /<id>) |
| `insertar_pagament.php` | `routes/pagaments.py` (POST /) |
| `llista_pagaments.php` | `routes/pagaments.py` (GET /) |
| `info_faller_pagament.php` | `routes/pagaments.py` (GET /info/<id>) |
| `percentatge.php` | `routes/stats.py` (GET /percentatge) |
| `total_quotes.php` | `routes/stats.py` (GET /total-quotes) |

### Actualizar el Frontend

Para que el frontend React use el nuevo backend Python, actualiza las URLs en los archivos correspondientes:

**Antes (PHP):**
```javascript
const url = 'http://localhost/gestio_falla_pare_castells_python/src/controller/llista_fallers.php';
```

**Después (Python):**
```javascript
const url = 'http://localhost:5000/api/fallers';
```

## 🧪 Pruebas

Puedes probar los endpoints con curl o Postman:

```bash
# Health check
curl http://localhost:5000/api/health

# Obtener todos los fallers
curl http://localhost:5000/api/fallers

# Crear un faller
curl -X POST http://localhost:5000/api/fallers \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Juan",
    "cognoms": "García López",
    "domicili": "C/ Principal 123",
    "telefon": "123456789",
    "dni": "12345678A",
    "data_naixement": "1990-01-01",
    "email": "juan@example.com",
    "edat": 34,
    "grup": "Fallers/falleres de brussó",
    "colaborador": 0,
    "data_alta": "2024-01-01",
    "categoria": "Home"
  }'
```

## 🛠️ Tecnologías Utilizadas

- **Flask**: Framework web ligero y flexible
- **Flask-CORS**: Manejo de CORS para integración con frontend
- **PyMySQL**: Conector MySQL para Python
- **python-dotenv**: Gestión de variables de entorno

## 📝 Notas Importantes

1. **Puerto**: El backend se ejecuta en el puerto `5000` por defecto
2. **CORS**: Configurado para aceptar peticiones desde cualquier origen en desarrollo
3. **Base de datos**: Usa la misma base de datos que la versión PHP
4. **Tarifas**: La lógica de cálculo de tarifas está en `utils/tariffs.py`

## 🐛 Solución de Problemas

### Error de conexión a la base de datos

- Verifica que MySQL esté ejecutándose
- Confirma las credenciales en el archivo `.env`
- Asegúrate de que la base de datos `pare_castells` exista

### Módulo no encontrado

```bash
pip install -r requirements.txt
```

### Puerto en uso

Cambia el puerto en `app.py` o cierra la aplicación que esté usando el puerto 5000.

## 📄 Licencia

Este proyecto es parte del sistema de gestión de la Falla Pare Castells.

## 👥 Contribuciones

Para contribuciones o reportar problemas, contacta con el equipo de desarrollo.
