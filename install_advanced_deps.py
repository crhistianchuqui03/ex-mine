#!/usr/bin/env python3
"""
Script para instalar dependencias adicionales para las mejoras avanzadas
"""

import subprocess
import sys

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando {package}: {e}")
        return False

def main():
    print("🚀 Instalando dependencias para News Aggregator Pro...")
    
    # Dependencias básicas ya instaladas
    basic_deps = [
        "flask",
        "flask-sqlalchemy", 
        "feedparser",
        "beautifulsoup4",
        "requests",
        "dateparser",
        "pandas"
    ]
    
    # Dependencias adicionales para mejoras avanzadas
    advanced_deps = [
        "redis",           # Para cache
        "celery",          # Para tareas asíncronas
        "schedule",        # Para scheduler automático
        "textblob",        # Para análisis de sentimientos
        "wordcloud",       # Para nubes de palabras
        "matplotlib",      # Para gráficos avanzados
        "seaborn",         # Para visualizaciones
        "plotly",          # Para gráficos interactivos
        "dash",            # Para dashboards interactivos
        "gunicorn",        # Para producción
        "python-dotenv",   # Para variables de entorno
        "flask-cors",      # Para CORS
        "flask-limiter",   # Para rate limiting
        "flask-caching",   # Para cache
        "flask-migrate",   # Para migraciones de DB
        "flask-mail",      # Para notificaciones por email
        "flask-socketio",  # Para WebSockets
        "psutil",          # Para monitoreo del sistema
        "prometheus-client", # Para métricas
        "sentry-sdk[flask]", # Para monitoreo de errores
    ]
    
    print("\n📦 Instalando dependencias básicas...")
    for dep in basic_deps:
        install_package(dep)
    
    print("\n🚀 Instalando dependencias avanzadas...")
    for dep in advanced_deps:
        install_package(dep)
    
    print("\n✨ ¡Instalación completada!")
    print("\n📋 Dependencias instaladas:")
    print("   • Redis - Cache en memoria")
    print("   • Celery - Tareas asíncronas")
    print("   • Schedule - Scheduler automático")
    print("   • TextBlob - Análisis de sentimientos")
    print("   • Matplotlib/Seaborn/Plotly - Gráficos avanzados")
    print("   • Dash - Dashboards interactivos")
    print("   • Gunicorn - Servidor de producción")
    print("   • Flask-CORS - CORS para API")
    print("   • Flask-Limiter - Rate limiting")
    print("   • Flask-Caching - Cache integrado")
    print("   • Flask-Migrate - Migraciones de DB")
    print("   • Flask-Mail - Notificaciones por email")
    print("   • Flask-SocketIO - WebSockets")
    print("   • PSUtil - Monitoreo del sistema")
    print("   • Prometheus - Métricas")
    print("   • Sentry - Monitoreo de errores")
    
    print("\n🎯 Próximos pasos:")
    print("   1. Ejecuta: python app.py")
    print("   2. Visita: http://127.0.0.1:8000")
    print("   3. ¡Disfruta de todas las nuevas funcionalidades!")

if __name__ == "__main__":
    main()
