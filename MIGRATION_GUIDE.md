# Guía de Migración Frontend - De PHP a Python Backend

## Cambios necesarios en el Frontend React

Para conectar el frontend con el nuevo backend Python, debes actualizar las URLs en los componentes que hacen peticiones HTTP.

### URL Base

**Antes (PHP en XAMPP):**
```javascript
const BASE_URL = 'http://localhost/gestio_falla_pare_castells_python/src/controller/';
```

**Después (Python Flask):**
```javascript
const BASE_URL = 'http://localhost:5000/api/';
```

### Mapeo de Endpoints

| Funcionalidad | URL PHP (Antigua) | URL Python (Nueva) |
|---------------|-------------------|-------------------|
| Listar fallers | `llista_fallers.php` | `fallers` |
| Obtener faller | `obtenir_faller.php?id={id}` | `fallers/{id}` |
| Crear faller | `insertar_fallers.php` | `fallers` (POST) |
| Modificar faller | `modificar_faller.php` | `fallers/{id}` (POST/PUT) |
| Listar pagaments | `llista_pagaments.php` | `pagaments` |
| Crear pagament | `insertar_pagament.php` | `pagaments` (POST) |
| Info faller pagament | `info_faller_pagament.php?id_faller={id}` | `pagaments/info/{id}` |
| Percentatge | `percentatge.php` | `stats/percentatge` |
| Total quotes | `total_quotes.php` | `stats/total-quotes` |

### Ejemplos de Actualización

#### 1. Listar Fallers (Llistar_fallers.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/llista_fallers.php');
```

**Después:**
```javascript
const response = await fetch('http://localhost:5000/api/fallers');
```

#### 2. Crear Faller (Donar_alta_fallers.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/insertar_fallers.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

**Después:**
```javascript
const response = await fetch('http://localhost:5000/api/fallers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

#### 3. Obtener Faller (Editar_fallers.jsx)

**Antes:**
```javascript
const response = await fetch(`http://localhost/gestio_falla_pare_castells_python/src/controller/obtenir_faller.php?id=${id}`);
```

**Después:**
```javascript
const response = await fetch(`http://localhost:5000/api/fallers/${id}`);
```

#### 4. Modificar Faller (Editar_fallers.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/modificar_faller.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

**Después:**
```javascript
const response = await fetch(`http://localhost:5000/api/fallers/${id}`, {
    method: 'POST', // o 'PUT'
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

#### 5. Crear Pagament (Pagaments.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/insertar_pagament.php', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

**Después:**
```javascript
const response = await fetch('http://localhost:5000/api/pagaments', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});
```

#### 6. Listar Pagaments (Llistar_pagaments.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/llista_pagaments.php');
```

**Después:**
```javascript
const response = await fetch('http://localhost:5000/api/pagaments');
```

#### 7. Percentatge (Percentatge.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/percentatge.php');
```

**Después:**
```javascript
const response = await fetch('http://localhost:5000/api/stats/percentatge');
```

#### 8. Total Quotes (Total_quotes.jsx)

**Antes:**
```javascript
const response = await fetch('http://localhost/gestio_falla_pare_castells_python/src/controller/total_quotes.php');
```

**Después:**
```javascript
const response = await fetch('http://localhost:5000/api/stats/total-quotes');
```

### Recomendación: Crear un archivo de configuración

Crea un archivo `src/config/api.js`:

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const API_ENDPOINTS = {
    // Fallers
    fallers: `${API_BASE_URL}/fallers`,
    getFaller: (id) => `${API_BASE_URL}/fallers/${id}`,
    
    // Pagaments
    pagaments: `${API_BASE_URL}/pagaments`,
    infoFallerPagament: (id) => `${API_BASE_URL}/pagaments/info/${id}`,
    
    // Stats
    percentatge: `${API_BASE_URL}/stats/percentatge`,
    totalQuotes: `${API_BASE_URL}/stats/total-quotes`,
    
    // Health
    health: `${API_BASE_URL}/health`
};

export default API_ENDPOINTS;
```

Luego en `.env` (raíz del proyecto):
```env
VITE_API_URL=http://localhost:5000/api
```

Y usar en los componentes:
```javascript
import API_ENDPOINTS from '../config/api';

const response = await fetch(API_ENDPOINTS.fallers);
```

### Verificación

1. Asegúrate de que el backend Python esté ejecutándose (`python app.py`)
2. Prueba cada endpoint con el frontend
3. Verifica que las respuestas JSON sean compatibles
4. Revisa la consola del navegador por errores CORS

### Notas

- El backend Python mantiene la misma estructura de respuestas JSON que PHP
- CORS ya está configurado en el backend Python
- Los métodos HTTP son los mismos (GET, POST, PUT, DELETE)
