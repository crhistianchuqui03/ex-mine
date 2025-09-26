#!/usr/bin/env python3
"""
Monitor del sistema para News Aggregator Pro
Monitorea recursos del sistema, base de datos y rendimiento
"""

import sys
import os
import logging
import json
from datetime import datetime, timedelta

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Article, Link
from config_advanced import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil no disponible. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

def get_system_metrics():
    """Obtiene métricas del sistema"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memoria
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_available = memory.available / (1024**3)  # GB
        memory_total = memory.total / (1024**3)  # GB
        
        # Disco
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_free = disk.free / (1024**3)  # GB
        disk_total = disk.total / (1024**3)  # GB
        
        # Red
        network = psutil.net_io_counters()
        
        # Procesos
        processes = len(psutil.pids())
        
        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count
            },
            'memory': {
                'percent': memory_percent,
                'available_gb': round(memory_available, 2),
                'total_gb': round(memory_total, 2)
            },
            'disk': {
                'percent': disk_percent,
                'free_gb': round(disk_free, 2),
                'total_gb': round(disk_total, 2)
            },
            'network': {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            },
            'processes': processes
        }
        
        return metrics
        
    except Exception as e:
        logging.error(f"Error obteniendo métricas del sistema: {e}")
        return None

def get_database_metrics():
    """Obtiene métricas de la base de datos"""
    try:
        with app.app_context():
            # Contar registros
            total_articles = Article.query.count()
            total_links = Link.query.count()
            
            # Artículos por fuente
            articles_by_source = db.session.query(
                Article.source, 
                db.func.count(Article.id)
            ).group_by(Article.source).all()
            
            # Artículos recientes (últimas 24 horas)
            recent_cutoff = datetime.utcnow() - timedelta(hours=24)
            recent_articles = Article.query.filter(
                Article.created_at >= recent_cutoff
            ).count()
            
            # Tamaño de la base de datos
            db_size = 0
            try:
                db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
                if os.path.exists(db_path):
                    db_size = os.path.getsize(db_path) / (1024**2)  # MB
            except:
                pass
            
            # Artículos por día (últimos 7 días)
            daily_stats = []
            for i in range(7):
                day_start = datetime.utcnow() - timedelta(days=i+1)
                day_end = datetime.utcnow() - timedelta(days=i)
                count = Article.query.filter(
                    Article.created_at >= day_start,
                    Article.created_at < day_end
                ).count()
                daily_stats.append({
                    'date': day_start.strftime('%Y-%m-%d'),
                    'count': count
                })
            
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'total_articles': total_articles,
                'total_links': total_links,
                'recent_articles_24h': recent_articles,
                'articles_by_source': dict(articles_by_source),
                'database_size_mb': round(db_size, 2),
                'daily_stats': daily_stats
            }
            
            return metrics
            
    except Exception as e:
        logging.error(f"Error obteniendo métricas de base de datos: {e}")
        return None

def get_application_metrics():
    """Obtiene métricas de la aplicación"""
    try:
        with app.app_context():
            # Verificar estado de las fuentes RSS
            source_status = {}
            for source_key in app.config.get('RSS_SOURCES', {}).keys():
                # Verificar si hay artículos recientes de esta fuente
                recent_cutoff = datetime.utcnow() - timedelta(hours=6)
                recent_count = Article.query.filter(
                    Article.source == source_key,
                    Article.created_at >= recent_cutoff
                ).count()
                
                source_status[source_key] = {
                    'recent_articles': recent_count,
                    'status': 'active' if recent_count > 0 else 'inactive'
                }
            
            # Verificar análisis de sentimientos
            sentiment_analyzed = 0
            try:
                sentiment_analyzed = Article.query.filter(
                    Article.sentiment_data.isnot(None)
                ).count()
            except:
                pass
            
            # Verificar favoritos
            favorites_count = 0
            try:
                favorites_count = Article.query.filter(
                    Article.is_favorite == True
                ).count()
            except:
                pass
            
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'source_status': source_status,
                'sentiment_analyzed': sentiment_analyzed,
                'favorites_count': favorites_count,
                'app_version': '1.0.0',
                'config_loaded': True
            }
            
            return metrics
            
    except Exception as e:
        logging.error(f"Error obteniendo métricas de aplicación: {e}")
        return None

def check_alerts(metrics):
    """Verifica alertas basadas en las métricas"""
    alerts = []
    
    if not metrics:
        return alerts
    
    # Alertas de sistema
    if 'system' in metrics:
        sys_metrics = metrics['system']
        
        # CPU alto
        if sys_metrics['cpu']['percent'] > 80:
            alerts.append({
                'type': 'warning',
                'message': f"CPU usage alto: {sys_metrics['cpu']['percent']}%",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Memoria alta
        if sys_metrics['memory']['percent'] > 85:
            alerts.append({
                'type': 'warning',
                'message': f"Memoria usage alto: {sys_metrics['memory']['percent']}%",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Disco lleno
        if sys_metrics['disk']['percent'] > 90:
            alerts.append({
                'type': 'critical',
                'message': f"Disco casi lleno: {sys_metrics['disk']['percent']}%",
                'timestamp': datetime.utcnow().isoformat()
            })
    
    # Alertas de base de datos
    if 'database' in metrics:
        db_metrics = metrics['database']
        
        # Sin artículos recientes
        if db_metrics['recent_articles_24h'] == 0:
            alerts.append({
                'type': 'warning',
                'message': "No hay artículos nuevos en las últimas 24 horas",
                'timestamp': datetime.utcnow().isoformat()
            })
        
        # Base de datos muy grande
        if db_metrics['database_size_mb'] > 1000:  # 1GB
            alerts.append({
                'type': 'info',
                'message': f"Base de datos grande: {db_metrics['database_size_mb']}MB",
                'timestamp': datetime.utcnow().isoformat()
            })
    
    return alerts

def save_metrics(metrics):
    """Guarda las métricas en un archivo JSON"""
    try:
        metrics_file = 'metrics.json'
        
        # Cargar métricas existentes
        existing_metrics = []
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                existing_metrics = json.load(f)
        
        # Agregar nuevas métricas
        existing_metrics.append(metrics)
        
        # Mantener solo las últimas 1000 entradas
        if len(existing_metrics) > 1000:
            existing_metrics = existing_metrics[-1000:]
        
        # Guardar
        with open(metrics_file, 'w') as f:
            json.dump(existing_metrics, f, indent=2)
        
        logging.info("✅ Métricas guardadas en metrics.json")
        
    except Exception as e:
        logging.error(f"Error guardando métricas: {e}")

def main():
    """Función principal del monitor"""
    logging.info("📊 Iniciando monitor del sistema...")
    
    # Obtener métricas
    system_metrics = get_system_metrics()
    database_metrics = get_database_metrics()
    application_metrics = get_application_metrics()
    
    # Combinar métricas
    all_metrics = {
        'system': system_metrics,
        'database': database_metrics,
        'application': application_metrics
    }
    
    # Verificar alertas
    alerts = check_alerts(all_metrics)
    
    # Mostrar métricas
    if system_metrics:
        logging.info("🖥️ Métricas del sistema:")
        logging.info(f"   CPU: {system_metrics['cpu']['percent']}% ({system_metrics['cpu']['count']} cores)")
        logging.info(f"   Memoria: {system_metrics['memory']['percent']}% ({system_metrics['memory']['available_gb']:.1f}GB libres)")
        logging.info(f"   Disco: {system_metrics['disk']['percent']}% ({system_metrics['disk']['free_gb']:.1f}GB libres)")
        logging.info(f"   Procesos: {system_metrics['processes']}")
    
    if database_metrics:
        logging.info("🗄️ Métricas de base de datos:")
        logging.info(f"   Artículos totales: {database_metrics['total_articles']}")
        logging.info(f"   Links totales: {database_metrics['total_links']}")
        logging.info(f"   Artículos recientes (24h): {database_metrics['recent_articles_24h']}")
        logging.info(f"   Tamaño DB: {database_metrics['database_size_mb']}MB")
    
    if application_metrics:
        logging.info("🚀 Métricas de aplicación:")
        logging.info(f"   Análisis de sentimientos: {application_metrics['sentiment_analyzed']}")
        logging.info(f"   Favoritos: {application_metrics['favorites_count']}")
    
    # Mostrar alertas
    if alerts:
        logging.info("⚠️ Alertas:")
        for alert in alerts:
            logging.info(f"   [{alert['type'].upper()}] {alert['message']}")
    else:
        logging.info("✅ Sin alertas")
    
    # Guardar métricas
    save_metrics(all_metrics)
    
    logging.info("✅ Monitor completado")

if __name__ == "__main__":
    main()
