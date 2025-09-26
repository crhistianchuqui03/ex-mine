# 🚀 News Aggregator Pro - Dashboard Avanzado

Una aplicación Flask avanzada para agregar, analizar y gestionar noticias de múltiples fuentes RSS con funcionalidades profesionales.

## ✨ Características Principales

### 📊 Dashboard Inteligente
- **Estadísticas en tiempo real**: Total de artículos, links, actividad diaria/semanal
- **Gráficos interactivos**: Distribución por fuente, top autores, secciones más populares
- **Métricas visuales**: Barras de progreso animadas y tarjetas informativas

### 🔍 Búsqueda Avanzada
- **Búsqueda inteligente**: En título, resumen y contenido completo
- **Filtros múltiples**: Por fuente, autor, sección, rango de fechas
- **Resultados paginados**: Navegación eficiente por grandes volúmenes de datos

### ⭐ Sistema de Favoritos
- **Marcado individual**: Botón de favorito en cada artículo
- **Acciones masivas**: Marcar/desmarcar múltiples artículos
- **Persistencia**: Los favoritos se mantienen entre sesiones

### 🎨 Interfaz Moderna
- **Modo oscuro/claro**: Toggle con persistencia de preferencias
- **Diseño responsivo**: Optimizado para móviles y tablets
- **Animaciones suaves**: Transiciones y efectos visuales profesionales
- **Tema personalizable**: Variables CSS para fácil personalización

### 📦 Acciones en Lote
- **Selección múltiple**: Checkboxes para seleccionar varios artículos
- **Operaciones masivas**: Eliminar, marcar favoritos en lote
- **Interfaz intuitiva**: Barra de acciones que aparece al seleccionar

### 🔄 Automatización
- **Scheduler automático**: Actualización programada de fuentes RSS
- **Limpieza automática**: Eliminación de artículos antiguos
- **Reportes diarios**: Estadísticas automáticas por email

### 🧠 Análisis de Sentimientos
- **Clasificación automática**: Positivo, negativo, neutral
- **Métricas de polaridad**: Análisis cuantitativo del tono
- **Estadísticas emocionales**: Distribución de sentimientos

### 📈 Monitoreo del Sistema
- **Métricas de rendimiento**: CPU, memoria, disco, red
- **Alertas automáticas**: Notificaciones por problemas del sistema
- **Logs detallados**: Seguimiento completo de actividades

## 🛠️ Instalación y Configuración

### 1. Instalar Dependencias Básicas
```bash
pip install flask flask-sqlalchemy feedparser beautifulsoup4 requests dateparser pandas
```

### 2. Instalar Dependencias Avanzadas
```bash
python install_advanced_deps.py
```

### 3. Configurar Variables de Entorno (Opcional)
```bash
# Crear archivo .env
echo "PORT=8000" > .env
echo "SECRET_KEY=tu-clave-secreta" >> .env
echo "REDIS_URL=redis://localhost:6379/0" >> .env
```

### 4. Ejecutar la Aplicación
```bash
# Aplicación principal
python app.py

# Scheduler automático (en terminal separado)
python scheduler.py

# Análisis de sentimientos (en terminal separado)
python sentiment_analyzer.py

# Monitor del sistema (en terminal separado)
python monitor.py
```

## 🌐 Acceso a la Aplicación

- **Aplicación principal**: http://127.0.0.1:8000
- **Búsqueda avanzada**: http://127.0.0.1:8000/search
- **API REST**: http://127.0.0.1:8000/api/articles
- **Vista de base de datos**: http://127.0.0.1:8000/admin/db

## 📋 Fuentes RSS Configuradas

| Fuente | URL | Idioma | Categoría |
|--------|-----|--------|-----------|
| BBC Mundo | https://feeds.bbci.co.uk/mundo/rss.xml | ES | Internacional |
| El País América | https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/america | ES | Internacional |
| El Universal | https://www.eluniversal.com.mx/rss.xml | ES | Nacional |
| CNN Español | https://cnnespanol.cnn.com/feed/ | ES | Internacional |
| Infobae | https://www.infobae.com/feeds/rss/ | ES | Nacional |

## 🔧 Funcionalidades Avanzadas

### API REST
```bash
# Obtener artículos con paginación
GET /api/articles?page=1&per_page=20&source=bbc_mundo

# Respuesta JSON con metadatos de paginación
{
  "articles": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

### Exportación de Datos
- **CSV**: Descarga completa con todos los campos
- **JSON**: Formato estructurado para integración
- **Filtros**: Exportar solo artículos seleccionados

### Análisis de Sentimientos
```python
# Ejemplo de análisis
sentiment_data = {
    'polarity': 0.2,      # -1 (negativo) a 1 (positivo)
    'subjectivity': 0.6,  # 0 (objetivo) a 1 (subjetivo)
    'sentiment': 'positive',
    'analyzed_at': '2024-01-15T10:30:00Z'
}
```

### Monitoreo del Sistema
```python
# Métricas disponibles
system_metrics = {
    'cpu': {'percent': 45, 'count': 8},
    'memory': {'percent': 60, 'available_gb': 6.4},
    'disk': {'percent': 25, 'free_gb': 150.2},
    'network': {'bytes_sent': 1024000, 'bytes_recv': 2048000}
}
```

## 🎯 Casos de Uso

### Para Periodistas
- **Monitoreo de fuentes**: Seguimiento de múltiples medios
- **Análisis de tendencias**: Identificación de temas trending
- **Investigación**: Búsqueda avanzada en archivos históricos

### Para Investigadores
- **Análisis de sentimientos**: Estudios de opinión pública
- **Datos estructurados**: Exportación para análisis estadístico
- **Tendencias temporales**: Evolución de temas en el tiempo

### Para Desarrolladores
- **API REST**: Integración con otras aplicaciones
- **Webhooks**: Notificaciones automáticas
- **Datos en tiempo real**: Streaming de noticias

## 🔒 Seguridad y Rendimiento

### Características de Seguridad
- **Rate limiting**: Protección contra abuso de API
- **Validación de entrada**: Sanitización de datos RSS
- **CORS configurado**: Control de acceso cross-origin
- **Sesiones seguras**: Cookies HTTPOnly y Secure

### Optimizaciones de Rendimiento
- **Cache Redis**: Respuestas frecuentes en memoria
- **Paginación**: Carga eficiente de grandes datasets
- **Lazy loading**: Carga bajo demanda de contenido
- **Compresión**: Respuestas HTTP comprimidas

## 📊 Métricas y Analytics

### Dashboard de Estadísticas
- **Artículos por fuente**: Distribución porcentual
- **Top autores**: Ranking de productividad
- **Secciones populares**: Categorías más activas
- **Tendencias temporales**: Evolución diaria/semanal

### Monitoreo del Sistema
- **Uso de recursos**: CPU, memoria, disco
- **Rendimiento de DB**: Tiempo de consultas
- **Alertas automáticas**: Notificaciones por problemas
- **Logs estructurados**: Seguimiento detallado

## 🚀 Despliegue en Producción

### Usando Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Usando Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

### Variables de Entorno para Producción
```bash
export FLASK_ENV=production
export SECRET_KEY=clave-super-secreta
export DATABASE_URL=postgresql://user:pass@localhost/newsdb
export REDIS_URL=redis://localhost:6379/0
export MAIL_SERVER=smtp.gmail.com
export MAIL_USERNAME=tu-email@gmail.com
export MAIL_PASSWORD=tu-password
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

- **Issues**: Reporta bugs o solicita features en GitHub Issues
- **Documentación**: Consulta la documentación completa en `/docs`
- **Comunidad**: Únete a nuestro Discord para soporte en tiempo real

## 🎉 Agradecimientos

- **Flask**: Framework web minimalista y flexible
- **SQLAlchemy**: ORM potente para Python
- **TextBlob**: Análisis de sentimientos en texto
- **Redis**: Cache y almacenamiento en memoria
- **Bootstrap**: Framework CSS para diseño responsivo

---

**¡Disfruta explorando las noticias con News Aggregator Pro! 🚀📰**
