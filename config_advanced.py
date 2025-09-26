"""
Configuración avanzada para News Aggregator Pro
"""

import os
from datetime import timedelta

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///news.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutos
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/1'
    RATELIMIT_DEFAULT = "100 per hour"
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'noreply@newsaggregator.com'
    
    # Celery configuration
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/2'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/3'
    
    # Sentry configuration
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    # Auto-refresh configuration
    AUTO_REFRESH_INTERVAL = int(os.environ.get('AUTO_REFRESH_INTERVAL') or 300)  # 5 minutos
    MAX_ARTICLES_PER_SOURCE = int(os.environ.get('MAX_ARTICLES_PER_SOURCE') or 20)
    
    # Cleanup configuration
    CLEANUP_DAYS = int(os.environ.get('CLEANUP_DAYS') or 30)  # Eliminar artículos más antiguos de 30 días
    
    # Analytics configuration
    ANALYTICS_ENABLED = os.environ.get('ANALYTICS_ENABLED', 'true').lower() in ['true', 'on', '1']
    ANALYTICS_RETENTION_DAYS = int(os.environ.get('ANALYTICS_RETENTION_DAYS') or 90)
    
    # Sentiment analysis
    SENTIMENT_ANALYSIS_ENABLED = os.environ.get('SENTIMENT_ANALYSIS_ENABLED', 'true').lower() in ['true', 'on', '1']
    
    # Dashboard configuration
    DASHBOARD_REFRESH_INTERVAL = int(os.environ.get('DASHBOARD_REFRESH_INTERVAL') or 30)  # 30 segundos
    
    # Export configuration
    MAX_EXPORT_ITEMS = int(os.environ.get('MAX_EXPORT_ITEMS') or 1000)
    
    # Security
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'false').lower() in ['true', 'on', '1']
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # WebSocket
    SOCKETIO_ASYNC_MODE = 'threading'
    
    # Monitoring
    MONITORING_ENABLED = os.environ.get('MONITORING_ENABLED', 'true').lower() in ['true', 'on', '1']
    METRICS_PORT = int(os.environ.get('METRICS_PORT') or 9090)

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    TESTING = False
    CACHE_TYPE = 'simple'  # Cache simple para desarrollo
    CELERY_TASK_ALWAYS_EAGER = True  # Ejecutar tareas síncronamente en desarrollo

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = 'simple'
    CELERY_TASK_ALWAYS_EAGER = True
    WTF_CSRF_ENABLED = False

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# RSS Sources con configuración avanzada
RSS_SOURCES_ADVANCED = {
    "bbc_mundo": {
        "name": "BBC Mundo",
        "url": "https://feeds.bbci.co.uk/mundo/rss.xml",
        "language": "es",
        "website": "https://www.bbc.com/mundo",
        "enabled": True,
        "priority": 1,
        "category": "internacional",
        "update_interval": 300,  # 5 minutos
        "max_articles": 20
    },
    "elpais_america": {
        "name": "El País América",
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/america",
        "language": "es",
        "website": "https://elpais.com/america",
        "enabled": True,
        "priority": 2,
        "category": "internacional",
        "update_interval": 600,  # 10 minutos
        "max_articles": 15
    },
    "el_universal": {
        "name": "El Universal (México)",
        "url": "https://www.eluniversal.com.mx/rss.xml",
        "language": "es",
        "website": "https://www.eluniversal.com.mx",
        "enabled": True,
        "priority": 3,
        "category": "nacional",
        "update_interval": 600,
        "max_articles": 15
    },
    "cnn_espanol": {
        "name": "CNN en Español",
        "url": "https://cnnespanol.cnn.com/feed/",
        "language": "es",
        "website": "https://cnnespanol.cnn.com",
        "enabled": True,
        "priority": 4,
        "category": "internacional",
        "update_interval": 300,
        "max_articles": 20
    },
    "infobae": {
        "name": "Infobae",
        "url": "https://www.infobae.com/feeds/rss/",
        "language": "es",
        "website": "https://www.infobae.com",
        "enabled": True,
        "priority": 5,
        "category": "nacional",
        "update_interval": 300,
        "max_articles": 20
    }
}

# Categorías de noticias
NEWS_CATEGORIES = {
    "internacional": "🌍 Internacional",
    "nacional": "🏛️ Nacional", 
    "economia": "💰 Economía",
    "tecnologia": "💻 Tecnología",
    "deportes": "⚽ Deportes",
    "cultura": "🎭 Cultura",
    "salud": "🏥 Salud",
    "ciencia": "🔬 Ciencia"
}

# Configuración de análisis de sentimientos
SENTIMENT_CONFIG = {
    "enabled": True,
    "thresholds": {
        "positive": 0.1,
        "negative": -0.1,
        "neutral": 0.0
    },
    "languages": ["es", "en"],
    "update_interval": 3600  # 1 hora
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    "email": {
        "enabled": True,
        "daily_summary": True,
        "breaking_news": True,
        "max_per_day": 10
    },
    "push": {
        "enabled": False,  # Requiere configuración adicional
        "vapid_public_key": os.environ.get('VAPID_PUBLIC_KEY'),
        "vapid_private_key": os.environ.get('VAPID_PRIVATE_KEY'),
        "vapid_claims": {"sub": "mailto:admin@newsaggregator.com"}
    }
}

# Configuración de exportación
EXPORT_CONFIG = {
    "formats": ["csv", "json", "xlsx", "pdf"],
    "max_items": 1000,
    "compression": True,
    "include_metadata": True
}

# Configuración de API
API_CONFIG = {
    "version": "v1",
    "rate_limit": "100 per hour",
    "pagination": {
        "default_per_page": 20,
        "max_per_page": 100
    },
    "caching": {
        "enabled": True,
        "timeout": 300
    }
}
