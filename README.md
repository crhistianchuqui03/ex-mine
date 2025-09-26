# 📰 Agregador de Noticias RSS

Una aplicación web moderna desarrollada en Flask que permite agregar, gestionar y analizar noticias de múltiples fuentes RSS de diferentes países de habla hispana.

## 🚀 Acceso a la Aplicación

### **Ruta Principal:**
```
http://localhost:5000/
```

### **Cómo Ejecutar:**
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecutar la aplicación:
   ```bash
   python app.py
   ```

3. Abrir en el navegador:
   ```
   http://localhost:5000/
   ```

## 🎯 ¿Para Qué Sirve Esta Página Web?

### **Funcionalidades Principales:**

#### 📰 **Agregación de Noticias RSS**
- **Fuentes Internacionales:** BBC Mundo, CNN en Español
- **Perú:** El Comercio, RPP Noticias, Perú21
- **Colombia:** El Tiempo (Nacional y Mundo)
- **España:** El País
- **Argentina:** Clarín, Infobae
- **República Dominicana:** Diario Libre (Portada, Economía, Política)
- **México:** El Universal, El País América

#### 🔍 **Búsqueda y Filtrado Avanzado**
- Búsqueda por texto en títulos, resúmenes y contenido
- Filtros por fuente, autor, sección y fechas
- Filtrado por temas específicos (economía, política, salud, tecnología, etc.)

#### ⭐ **Gestión de Contenido**
- Sistema de favoritos para marcar artículos importantes
- Eliminación individual o masiva de artículos
- Vista detallada con contenido extendido

#### 📊 **Análisis y Estadísticas**
- Dashboard con estadísticas en tiempo real
- Contadores de artículos por fuente
- Top autores y secciones más populares
- Artículos del día y de la semana

#### 📥 **Exportación de Datos**
- Descarga en formato CSV
- Exportación en formato JSON
- Descargas históricas por fecha
- Filtros personalizados para exportación

#### 🔄 **Actualización Automática**
- Actualización manual de fuentes específicas
- Actualización masiva de todas las fuentes
- Configuración de límites y filtros de tiempo
- Procesamiento inteligente de contenido

## 🛠️ Características Técnicas

### **Tecnologías Utilizadas:**
- **Backend:** Flask (Python)
- **Base de Datos:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Procesamiento:** BeautifulSoup, Feedparser
- **Análisis:** Pandas (opcional)

### **Arquitectura:**
- **Modelo:** SQLAlchemy ORM
- **Vistas:** Templates Jinja2
- **Controladores:** Rutas Flask
- **API:** Endpoints REST para integración

## 📱 Interfaz de Usuario

### **Página Principal:**
- Dashboard con estadísticas generales
- Lista de artículos más recientes
- Panel de control para actualizar fuentes
- Accesos rápidos a funciones principales

### **Funciones Disponibles:**
- ✅ Agregar enlaces manualmente
- ✅ Actualizar noticias RSS
- ✅ Buscar y filtrar contenido
- ✅ Marcar/desmarcar favoritos
- ✅ Eliminar artículos
- ✅ Descargar datos
- ✅ Vista administrativa de base de datos

## 🔧 Configuración Avanzada

### **Variables de Entorno:**
```bash
PORT=5000  # Puerto de la aplicación
```

### **Base de Datos:**
- Archivo: `news.db`
- Tablas: `articles`, `links`
- Migración automática de esquemas

### **Fuentes RSS Configurables:**
- Agregar nuevas fuentes en `RSS_SOURCES`
- Configurar idioma y región
- Personalizar límites de artículos

## 📈 Casos de Uso

### **Para Periodistas:**
- Monitoreo de múltiples fuentes de noticias
- Análisis de tendencias por región
- Exportación de datos para reportes

### **Para Investigadores:**
- Recopilación de datos históricos
- Análisis de contenido por temas
- Extracción de metadatos (autor, fecha, sección)

### **Para Desarrolladores:**
- API REST para integración
- Datos estructurados en JSON/CSV
- Código fuente modular y extensible

## 🚀 Despliegue

### **Desarrollo Local:**
```bash
python app.py
# Acceso: http://localhost:5000/
```

### **Producción:**
```bash
# Usando Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📋 Requisitos del Sistema

- Python 3.7+
- Flask 2.0+
- SQLite3
- Conexión a Internet (para RSS)

## 🤝 Contribuciones

Este proyecto está abierto a contribuciones. Las áreas de mejora incluyen:
- Nuevas fuentes RSS
- Mejoras en la interfaz
- Optimizaciones de rendimiento
- Nuevas funcionalidades de análisis

## 📄 Licencia

Proyecto de código abierto para uso educativo y de investigación.

---

**Desarrollado con ❤️ usando Flask y tecnologías web modernas**