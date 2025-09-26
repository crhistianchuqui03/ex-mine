#!/usr/bin/env python3
"""
Script para generar datos históricos de ejemplo
Simula artículos de días/semanas anteriores
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Article, RSS_SOURCES

def generate_historical_articles():
    """Genera artículos históricos de ejemplo"""
    
    with app.app_context():
        print("🔄 Generando datos históricos de ejemplo...")
        
        # Fuentes disponibles
        sources = list(RSS_SOURCES.keys())
        
        # Generar artículos para los últimos 30 días
        articles_created = 0
        
        for days_ago in range(30):
            # Fecha del artículo
            article_date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Generar entre 2-8 artículos por día
            articles_per_day = random.randint(2, 8)
            
            for i in range(articles_per_day):
                # Seleccionar fuente aleatoria
                source = random.choice(sources)
                source_info = RSS_SOURCES[source]
                
                # Generar título de ejemplo
                titles = [
                    f"Noticia importante del {article_date.strftime('%d/%m/%Y')}",
                    f"Desarrollo tecnológico destacado - {article_date.strftime('%d de %B')}",
                    f"Análisis económico del día {article_date.strftime('%d/%m')}",
                    f"Actualización política - {article_date.strftime('%B %Y')}",
                    f"Reporte especial de {source_info['name']}",
                    f"Investigación científica del {article_date.strftime('%d/%m/%Y')}",
                    f"Tendencias sociales del {article_date.strftime('%d de %B')}",
                    f"Actualización internacional - {article_date.strftime('%d/%m')}"
                ]
                
                title = random.choice(titles)
                
                # Generar URL única
                url = f"https://{source_info['website'].replace('https://', '')}/noticia-{days_ago}-{i}-{random.randint(1000, 9999)}"
                
                # Verificar si ya existe
                if Article.query.filter_by(url=url).first():
                    continue
                
                # Generar resumen
                summaries = [
                    f"Este es un resumen de la noticia del {article_date.strftime('%d/%m/%Y')} que cubre aspectos importantes del tema.",
                    f"Análisis detallado de los eventos ocurridos el {article_date.strftime('%d de %B')} con información relevante.",
                    f"Reporte completo sobre los desarrollos del día {article_date.strftime('%d/%m')} con datos actualizados.",
                    f"Información actualizada sobre los acontecimientos del {article_date.strftime('%d de %B de %Y')}.",
                    f"Cobertura especial de los eventos del {article_date.strftime('%d/%m/%Y')} con análisis profundo."
                ]
                
                summary = random.choice(summaries)
                
                # Generar contenido extendido
                content_parts = [
                    f"En el día {article_date.strftime('%d de %B de %Y')}, se desarrollaron varios acontecimientos importantes.",
                    "Los expertos han analizado la situación y han llegado a conclusiones relevantes.",
                    "La información disponible sugiere que estos eventos tendrán un impacto significativo.",
                    "Se espera que en los próximos días se publiquen más detalles sobre este tema.",
                    "Los analistas coinciden en que esta situación requiere atención especial.",
                    "Las autoridades han emitido declaraciones oficiales sobre el tema.",
                    "La comunidad internacional ha reaccionado a estos desarrollos.",
                    "Se prevé que esta situación evolucione en las próximas semanas."
                ]
                
                content_long = " ".join(random.sample(content_parts, random.randint(4, 6)))
                
                # Generar autor
                authors = [
                    "Redacción", "Equipo Editorial", "Corresponsal", "Reportero",
                    "Analista", "Especialista", "Corresponsal Internacional"
                ]
                author = random.choice(authors)
                
                # Generar sección
                sections = [
                    "Internacional", "Nacional", "Economía", "Tecnología",
                    "Política", "Cultura", "Deportes", "Salud", "Ciencia"
                ]
                section = random.choice(sections)
                
                # Crear artículo
                article = Article(
                    url=url,
                    title=title,
                    date_iso=article_date.strftime('%Y-%m-%dT%H:%M:%S'),
                    summary=summary,
                    author=author,
                    section=section,
                    content_long=content_long,
                    source=source,
                    is_favorite=random.choice([True, False]),
                    created_at=article_date
                )
                
                try:
                    db.session.add(article)
                    db.session.commit()
                    articles_created += 1
                    
                    if articles_created % 10 == 0:
                        print(f"✅ {articles_created} artículos históricos creados...")
                        
                except Exception as e:
                    db.session.rollback()
                    print(f"❌ Error creando artículo: {e}")
                    continue
        
        print(f"\n🎉 ¡Generación completada!")
        print(f"📊 Total de artículos históricos creados: {articles_created}")
        print(f"📅 Período cubierto: Últimos 30 días")
        print(f"📰 Fuentes utilizadas: {len(sources)}")
        
        # Mostrar estadísticas
        total_articles = Article.query.count()
        print(f"\n📈 Estadísticas actuales:")
        print(f"   • Total de artículos en la base de datos: {total_articles}")
        
        # Artículos por fuente
        for source_key in sources:
            count = Article.query.filter_by(source=source_key).count()
            source_name = RSS_SOURCES[source_key]['name']
            print(f"   • {source_name}: {count} artículos")
        
        # Artículos por día (últimos 7 días)
        print(f"\n📅 Artículos por día (últimos 7 días):")
        for days_ago in range(7):
            day_date = datetime.utcnow() - timedelta(days=days_ago)
            day_start = day_date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            count = Article.query.filter(
                Article.created_at >= day_start,
                Article.created_at < day_end
            ).count()
            
            print(f"   • {day_date.strftime('%d/%m/%Y')}: {count} artículos")

def main():
    """Función principal"""
    print("🚀 Generador de Datos Históricos - News Aggregator Pro")
    print("=" * 60)
    
    try:
        generate_historical_articles()
        
        print("\n" + "=" * 60)
        print("🎯 Próximos pasos:")
        print("   1. Visita: http://127.0.0.1:8000")
        print("   2. Prueba las nuevas opciones de descarga histórica")
        print("   3. Usa los filtros de fecha en la búsqueda avanzada")
        print("   4. Descarga datos por períodos específicos")
        
    except Exception as e:
        print(f"❌ Error durante la generación: {e}")

if __name__ == "__main__":
    main()
