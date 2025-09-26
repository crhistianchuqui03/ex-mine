#!/usr/bin/env python3
"""
Analizador de sentimientos para News Aggregator Pro
Clasifica artículos por tono emocional (positivo, negativo, neutral)
"""

import sys
import os
import logging
from datetime import datetime, timedelta

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Article
from config_advanced import SENTIMENT_CONFIG

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    from textblob import TextBlob
    from textblob.sentiments import NaiveBayesAnalyzer
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logging.warning("TextBlob no disponible. Instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob"])
    from textblob import TextBlob
    from textblob.sentiments import NaiveBayesAnalyzer

def analyze_sentiment(text):
    """
    Analiza el sentimiento de un texto
    Retorna: {'polarity': float, 'subjectivity': float, 'sentiment': str}
    """
    if not text or len(text.strip()) < 10:
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral'
        }
    
    try:
        # Usar TextBlob para análisis básico
        blob = TextBlob(text)
        
        polarity = blob.sentiment.polarity  # -1 (negativo) a 1 (positivo)
        subjectivity = blob.sentiment.subjectivity  # 0 (objetivo) a 1 (subjetivo)
        
        # Clasificar sentimiento según umbrales
        thresholds = SENTIMENT_CONFIG['thresholds']
        
        if polarity > thresholds['positive']:
            sentiment = 'positive'
        elif polarity < thresholds['negative']:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment
        }
        
    except Exception as e:
        logging.error(f"Error analizando sentimiento: {e}")
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral'
        }

def analyze_article(article):
    """Analiza el sentimiento de un artículo completo"""
    if not SENTIMENT_CONFIG['enabled']:
        return None
    
    # Combinar título y resumen para análisis
    text_parts = []
    
    if article.title:
        text_parts.append(article.title)
    
    if article.summary:
        text_parts.append(article.summary)
    
    if article.content_long:
        # Usar solo los primeros 500 caracteres del contenido extendido
        text_parts.append(article.content_long[:500])
    
    combined_text = " ".join(text_parts)
    
    if not combined_text.strip():
        return None
    
    # Analizar sentimiento
    sentiment_data = analyze_sentiment(combined_text)
    
    # Agregar información adicional
    sentiment_data['analyzed_at'] = datetime.utcnow()
    sentiment_data['text_length'] = len(combined_text)
    sentiment_data['word_count'] = len(combined_text.split())
    
    return sentiment_data

def update_article_sentiment(article_id):
    """Actualiza el sentimiento de un artículo específico"""
    try:
        with app.app_context():
            article = Article.query.get(article_id)
            if not article:
                logging.warning(f"Artículo {article_id} no encontrado")
                return False
            
            # Verificar si ya tiene análisis de sentimiento
            if hasattr(article, 'sentiment_data') and article.sentiment_data:
                logging.info(f"Artículo {article_id} ya tiene análisis de sentimiento")
                return True
            
            # Analizar sentimiento
            sentiment_data = analyze_article(article)
            if not sentiment_data:
                logging.warning(f"No se pudo analizar el artículo {article_id}")
                return False
            
            # Guardar en la base de datos
            # Por ahora usamos un campo JSON simple, después se puede convertir en tabla separada
            try:
                import json
                article.sentiment_data = json.dumps(sentiment_data)
                db.session.commit()
                
                logging.info(f"✅ Sentimiento analizado para artículo {article_id}: {sentiment_data['sentiment']}")
                return True
                
            except Exception as e:
                # Si no existe la columna, la agregamos
                if "no such column" in str(e).lower():
                    try:
                        db.session.execute("ALTER TABLE articles ADD COLUMN sentiment_data TEXT")
                        db.session.commit()
                        logging.info("✅ Columna sentiment_data agregada")
                        
                        # Reintentar guardar
                        article.sentiment_data = json.dumps(sentiment_data)
                        db.session.commit()
                        
                        logging.info(f"✅ Sentimiento analizado para artículo {article_id}: {sentiment_data['sentiment']}")
                        return True
                        
                    except Exception as e2:
                        logging.error(f"Error agregando columna sentiment_data: {e2}")
                        db.session.rollback()
                        return False
                else:
                    logging.error(f"Error guardando sentimiento: {e}")
                    db.session.rollback()
                    return False
                    
    except Exception as e:
        logging.error(f"Error actualizando sentimiento del artículo {article_id}: {e}")
        return False

def analyze_recent_articles(hours=24):
    """Analiza el sentimiento de artículos recientes"""
    try:
        with app.app_context():
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            # Obtener artículos sin análisis de sentimiento
            articles = Article.query.filter(
                Article.created_at >= cutoff_time
            ).filter(
                db.or_(
                    Article.sentiment_data.is_(None),
                    Article.sentiment_data == ''
                )
            ).all()
            
            logging.info(f"Analizando sentimiento de {len(articles)} artículos recientes...")
            
            analyzed = 0
            for article in articles:
                if update_article_sentiment(article.id):
                    analyzed += 1
            
            logging.info(f"✅ {analyzed} artículos analizados exitosamente")
            return analyzed
            
    except Exception as e:
        logging.error(f"Error analizando artículos recientes: {e}")
        return 0

def get_sentiment_stats():
    """Obtiene estadísticas de sentimientos"""
    try:
        with app.app_context():
            import json
            
            # Contar por sentimiento
            sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0, 'unknown': 0}
            total_polarity = 0
            total_subjectivity = 0
            analyzed_count = 0
            
            articles = Article.query.filter(Article.sentiment_data.isnot(None)).all()
            
            for article in articles:
                try:
                    sentiment_data = json.loads(article.sentiment_data)
                    sentiment = sentiment_data.get('sentiment', 'unknown')
                    sentiment_counts[sentiment] += 1
                    
                    total_polarity += sentiment_data.get('polarity', 0)
                    total_subjectivity += sentiment_data.get('subjectivity', 0)
                    analyzed_count += 1
                    
                except (json.JSONDecodeError, KeyError):
                    sentiment_counts['unknown'] += 1
            
            # Calcular promedios
            avg_polarity = total_polarity / analyzed_count if analyzed_count > 0 else 0
            avg_subjectivity = total_subjectivity / analyzed_count if analyzed_count > 0 else 0
            
            stats = {
                'total_analyzed': analyzed_count,
                'sentiment_distribution': sentiment_counts,
                'average_polarity': round(avg_polarity, 3),
                'average_subjectivity': round(avg_subjectivity, 3),
                'last_updated': datetime.utcnow().isoformat()
            }
            
            return stats
            
    except Exception as e:
        logging.error(f"Error obteniendo estadísticas de sentimiento: {e}")
        return None

def main():
    """Función principal"""
    logging.info("🧠 Iniciando análisis de sentimientos...")
    
    if not SENTIMENT_CONFIG['enabled']:
        logging.info("Análisis de sentimientos deshabilitado en configuración")
        return
    
    # Analizar artículos recientes
    analyzed = analyze_recent_articles(24)
    
    # Mostrar estadísticas
    stats = get_sentiment_stats()
    if stats:
        logging.info("📊 Estadísticas de sentimientos:")
        logging.info(f"   Total analizados: {stats['total_analyzed']}")
        logging.info(f"   Promedio polaridad: {stats['average_polarity']}")
        logging.info(f"   Promedio subjetividad: {stats['average_subjectivity']}")
        logging.info("   Distribución:")
        for sentiment, count in stats['sentiment_distribution'].items():
            percentage = (count / stats['total_analyzed'] * 100) if stats['total_analyzed'] > 0 else 0
            logging.info(f"     {sentiment}: {count} ({percentage:.1f}%)")
    
    logging.info("✅ Análisis de sentimientos completado")

if __name__ == "__main__":
    main()
