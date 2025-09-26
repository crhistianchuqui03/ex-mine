#!/usr/bin/env python3
"""
Scheduler automático para News Aggregator Pro
Actualiza las fuentes RSS automáticamente según su configuración
"""

import schedule
import time
import logging
from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio actual al path para importar app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, fetch_articles_from_source, RSS_SOURCES, db, Article
from config_advanced import RSS_SOURCES_ADVANCED

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

def update_source(source_key):
    """Actualiza una fuente específica"""
    try:
        with app.app_context():
            source_config = RSS_SOURCES_ADVANCED.get(source_key, {})
            if not source_config.get('enabled', True):
                logging.info(f"Fuente {source_key} deshabilitada, saltando...")
                return
            
            max_articles = source_config.get('max_articles', 10)
            source_name = source_config.get('name', source_key)
            
            logging.info(f"Actualizando {source_name}...")
            nuevos = fetch_articles_from_source(source_key, max_articles)
            
            if nuevos > 0:
                logging.info(f"✅ {source_name}: {nuevos} artículos nuevos")
            else:
                logging.info(f"ℹ️ {source_name}: Sin artículos nuevos")
                
    except Exception as e:
        logging.error(f"❌ Error actualizando {source_key}: {e}")

def update_all_sources():
    """Actualiza todas las fuentes habilitadas"""
    logging.info("🔄 Iniciando actualización de todas las fuentes...")
    
    for source_key in RSS_SOURCES_ADVANCED.keys():
        update_source(source_key)
        time.sleep(2)  # Pequeña pausa entre fuentes
    
    logging.info("✅ Actualización completa finalizada")

def cleanup_old_articles():
    """Limpia artículos antiguos según la configuración"""
    try:
        with app.app_context():
            from config_advanced import Config
            cutoff_date = datetime.utcnow() - timedelta(days=Config.CLEANUP_DAYS)
            
            old_articles = Article.query.filter(Article.created_at < cutoff_date).all()
            count = len(old_articles)
            
            if count > 0:
                for article in old_articles:
                    db.session.delete(article)
                db.session.commit()
                logging.info(f"🗑️ Eliminados {count} artículos antiguos (> {Config.CLEANUP_DAYS} días)")
            else:
                logging.info("ℹ️ No hay artículos antiguos para eliminar")
                
    except Exception as e:
        logging.error(f"❌ Error en limpieza: {e}")

def generate_daily_report():
    """Genera un reporte diario de estadísticas"""
    try:
        with app.app_context():
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            yesterday = today - timedelta(days=1)
            
            # Estadísticas del día
            articles_today = Article.query.filter(Article.created_at >= today).count()
            articles_yesterday = Article.query.filter(
                Article.created_at >= yesterday,
                Article.created_at < today
            ).count()
            
            # Estadísticas por fuente
            sources_stats = db.session.query(
                Article.source, 
                db.func.count(Article.id)
            ).filter(Article.created_at >= today).group_by(Article.source).all()
            
            logging.info("📊 Reporte diario:")
            logging.info(f"   Artículos hoy: {articles_today}")
            logging.info(f"   Artículos ayer: {articles_yesterday}")
            logging.info("   Por fuente:")
            for source, count in sources_stats:
                source_name = RSS_SOURCES_ADVANCED.get(source, {}).get('name', source)
                logging.info(f"     {source_name}: {count}")
                
    except Exception as e:
        logging.error(f"❌ Error generando reporte: {e}")

def setup_scheduler():
    """Configura el scheduler con las tareas programadas"""
    logging.info("⏰ Configurando scheduler automático...")
    
    # Actualización de fuentes según su intervalo configurado
    for source_key, config in RSS_SOURCES_ADVANCED.items():
        if config.get('enabled', True):
            interval = config.get('update_interval', 300)  # 5 minutos por defecto
            
            if interval < 60:
                schedule.every(interval).seconds.do(update_source, source_key)
                logging.info(f"   {config['name']}: cada {interval} segundos")
            elif interval < 3600:
                minutes = interval // 60
                schedule.every(minutes).minutes.do(update_source, source_key)
                logging.info(f"   {config['name']}: cada {minutes} minutos")
            else:
                hours = interval // 3600
                schedule.every(hours).hours.do(update_source, source_key)
                logging.info(f"   {config['name']}: cada {hours} horas")
    
    # Actualización completa cada 2 horas
    schedule.every(2).hours.do(update_all_sources)
    
    # Limpieza diaria a las 3 AM
    schedule.every().day.at("03:00").do(cleanup_old_articles)
    
    # Reporte diario a las 8 AM
    schedule.every().day.at("08:00").do(generate_daily_report)
    
    logging.info("✅ Scheduler configurado correctamente")

def main():
    """Función principal del scheduler"""
    logging.info("🚀 Iniciando News Aggregator Scheduler...")
    
    # Configurar el scheduler
    setup_scheduler()
    
    # Ejecutar una actualización inicial
    logging.info("🔄 Ejecutando actualización inicial...")
    update_all_sources()
    
    # Ejecutar el scheduler
    logging.info("⏰ Scheduler iniciado. Presiona Ctrl+C para detener...")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("🛑 Scheduler detenido por el usuario")
    except Exception as e:
        logging.error(f"❌ Error en scheduler: {e}")

if __name__ == "__main__":
    main()
