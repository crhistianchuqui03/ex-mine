#!/usr/bin/env python3
"""
Script para descargar artículos de todas las fuentes RSS configuradas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, fetch_articles_from_source, RSS_SOURCES, db
from datetime import datetime

def download_all_sources():
    """Descarga artículos de todas las fuentes RSS"""
    print("🚀 Iniciando descarga masiva de noticias...")
    print("=" * 60)
    
    total_articles = 0
    
    with app.app_context():
        for source_key, source_info in RSS_SOURCES.items():
            print(f"\n📰 Procesando: {source_info['name']}")
            print(f"   URL: {source_info['url']}")
            print(f"   Web: {source_info['website']}")
            
            try:
                # Descargar 50 artículos por fuente para obtener más datos
                nuevos = fetch_articles_from_source(source_key, limit=50)
                total_articles += nuevos
                print(f"   ✅ {nuevos} artículos nuevos agregados")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                continue
    
    print("\n" + "=" * 60)
    print(f"🎉 Descarga completada!")
    print(f"📊 Total de artículos nuevos: {total_articles}")
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Mostrar estadísticas por fuente
    print("\n📈 Estadísticas por fuente:")
    with app.app_context():
        from app import Article
        for source_key, source_info in RSS_SOURCES.items():
            count = Article.query.filter_by(source=source_key).count()
            print(f"   {source_info['name']}: {count} artículos")

if __name__ == "__main__":
    download_all_sources()
