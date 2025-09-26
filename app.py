from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os
import csv
import json
import feedparser
from bs4 import BeautifulSoup
import dateparser, requests, time

# ---------- Config ----------
DB_PATH = Path("news.db").absolute()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "dev"  # cambia en prod
db = SQLAlchemy(app)

# ---------- Modelos ----------
class Link(db.Model):
    __tablename__ = "links"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Opcional: tabla artículos "enriquecida"
class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1000), nullable=False, unique=True)
    title = db.Column(db.String(1000))
    date_iso = db.Column(db.String(32))
    summary = db.Column(db.Text)
    author = db.Column(db.String(255))
    section = db.Column(db.String(255))
    # NUEVO: contenido extendido
    content_long = db.Column(db.Text)
    # NUEVO: fuente RSS
    source = db.Column(db.String(100))
    # NUEVO: favorito
    is_favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    # mini-migración para SQLite: agrega columnas si faltan
    try:
        from sqlalchemy import text
        cols = [r[1] for r in db.session.execute(text("PRAGMA table_info(articles)")).fetchall()]
        if "content_long" not in cols:
            db.session.execute(text("ALTER TABLE articles ADD COLUMN content_long TEXT"))
            db.session.commit()
            print("✅ Columna content_long agregada a la tabla articles")
        if "source" not in cols:
            db.session.execute(text("ALTER TABLE articles ADD COLUMN source TEXT"))
            db.session.commit()
            print("✅ Columna source agregada a la tabla articles")
        if "is_favorite" not in cols:
            db.session.execute(text("ALTER TABLE articles ADD COLUMN is_favorite BOOLEAN DEFAULT 0"))
            db.session.commit()
            print("✅ Columna is_favorite agregada a la tabla articles")
    except Exception as e:
        db.session.rollback()
        print(f"⚠️ Error en migración: {e}")

# ---------- Rutas ----------
@app.get("/")
def index():
    # Últimos guardados (para ver que funciona)
    recent_links = Link.query.order_by(Link.created_at.desc()).limit(10).all()
    recent_articles = Article.query.order_by(Article.created_at.desc()).all()  # Mostrar todos los artículos
    
    # Estadísticas para el dashboard
    stats = {
        'total_articles': Article.query.count(),
        'total_links': Link.query.count(),
        'articles_by_source': db.session.query(Article.source, db.func.count(Article.id)).group_by(Article.source).all(),
        'articles_today': Article.query.filter(Article.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)).count(),
        'articles_this_week': Article.query.filter(Article.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)).count(),
        'top_authors': db.session.query(Article.author, db.func.count(Article.id)).filter(Article.author.isnot(None)).group_by(Article.author).order_by(db.func.count(Article.id).desc()).limit(5).all(),
        'top_sections': db.session.query(Article.section, db.func.count(Article.id)).filter(Article.section.isnot(None)).group_by(Article.section).order_by(db.func.count(Article.id).desc()).limit(5).all()
    }
    
    return render_template("index.html", recent_links=recent_links, recent_articles=recent_articles, rss_sources=RSS_SOURCES, stats=stats)

@app.post("/add-link")
def add_link():
    url = (request.form.get("url") or "").strip()
    if not url:
        flash("Pega un enlace válido.", "error")
        return redirect(url_for("index"))

    # MODO A: guardar solo el link
    if request.form.get("modo") == "simple":
        try:
            if not Link.query.filter_by(url=url).first():
                db.session.add(Link(url=url))
                db.session.commit()
            flash("¡Link guardado!", "ok")
        except Exception as e:
            db.session.rollback()
            flash(f"Error guardando link: {e}", "error")
        return redirect(url_for("index"))

    # MODO B: enriquecer y guardar (BBC Mundo)
    # si quieres que *solo* BBC se acepte, puedes validar `if "bbc.com/mundo" not in url: ...`
    try:
        from bs4 import BeautifulSoup
        import requests, dateparser

        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # Título
        title = soup.title.get_text(" ", strip=True) if soup.title else None
        # Fecha desde meta si existe
        date_meta = (soup.find("meta", {"property": "article:published_time"}) or
                     soup.find("meta", {"name": "date"}))
        date_iso = None
        if date_meta and date_meta.get("content"):
            dt = dateparser.parse(date_meta["content"])
            if dt: date_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")

        # Resumen (fallback: primeros párrafos)
        desc_meta = (soup.find("meta", {"name": "description"}) or
                     soup.find("meta", {"property": "og:description"}))
        summary = desc_meta.get("content").strip() if desc_meta and desc_meta.get("content") else None
        if not summary:
            ps = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
            ps = [t for t in ps if len(t) > 30]
            if ps:
                summary = " ".join(ps[:4])

        # Contenido extendido (primeros ~12 párrafos)
        ps = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
        ps = [t for t in ps if len(t) > 30]
        content_long = " ".join(ps[:12]) if ps else None

        # Autor/sección si existen (búsqueda más exhaustiva)
        author = None
        author_meta = (soup.find("meta", {"name": "author"}) or
                      soup.find("meta", {"property": "article:author"}) or
                      soup.find("meta", {"name": "twitter:creator"}))
        if author_meta and author_meta.get("content"):
            author = author_meta["content"].strip()
        
        section = None
        section_meta = (soup.find("meta", {"property": "article:section"}) or
                       soup.find("meta", {"name": "section"}) or
                       soup.find("meta", {"property": "og:section"}))
        if section_meta and section_meta.get("content"):
            section = section_meta["content"].strip()

        if not Article.query.filter_by(url=url).first():
            db.session.add(Article(
                url=url,
                title=title,
                date_iso=date_iso,
                summary=summary,
                author=author,
                section=section,
                content_long=content_long,
            ))
        db.session.commit()
        flash("¡Artículo guardado/enriquecido!", "ok")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al enriquecer/guardar: {e}", "error")

    return redirect(url_for("index"))

# ---------- Fuentes RSS configuradas ----------
RSS_SOURCES = {
    # 🌍 INTERNACIONALES
    "bbc_mundo": {
        "name": "BBC Mundo",
        "url": "https://feeds.bbci.co.uk/mundo/rss.xml",
        "language": "es",
        "website": "https://www.bbc.com/mundo",
        "region": "Internacional"
    },
    "cnn_espanol": {
        "name": "CNN en Español",
        "url": "https://cnnespanol.cnn.com/feed/",
        "language": "es",
        "website": "https://cnnespanol.cnn.com",
        "region": "Internacional"
    },
    
    # 🇵🇪 PERÚ
    "el_comercio_peru": {
        "name": "El Comercio Perú",
        "url": "https://elcomercio.pe/rss/portada.xml",
        "language": "es",
        "website": "https://elcomercio.pe",
        "region": "Perú"
    },
    "rpp_noticias": {
        "name": "RPP Noticias",
        "url": "https://rpp.pe/noticias/rss",
        "language": "es",
        "website": "https://rpp.pe",
        "region": "Perú"
    },
    "peru21": {
        "name": "Perú21",
        "url": "https://peru21.pe/rss/portada.xml",
        "language": "es",
        "website": "https://peru21.pe",
        "region": "Perú"
    },
    
    # 🇨🇴 COLOMBIA
    "el_tiempo": {
        "name": "El Tiempo Colombia",
        "url": "https://www.eltiempo.com/rss",
        "language": "es",
        "website": "https://www.eltiempo.com",
        "region": "Colombia"
    },
    "el_tiempo_mundo": {
        "name": "El Tiempo Mundo",
        "url": "https://www.eltiempo.com/rss/mundo.xml",
        "language": "es",
        "website": "https://www.eltiempo.com",
        "region": "Colombia"
    },
    
    # 🇪🇸 ESPAÑA
    "elpais_portada": {
        "name": "El País Portada",
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
        "language": "es",
        "website": "https://elpais.com",
        "region": "España"
    },
    
    # 🇦🇷 ARGENTINA
    "clarin": {
        "name": "Clarín Argentina",
        "url": "https://www.clarin.com/rss/lo-ultimo/",
        "language": "es",
        "website": "https://www.clarin.com",
        "region": "Argentina"
    },
    "infobae": {
        "name": "Infobae Argentina",
        "url": "https://www.infobae.com/feeds/rss/",
        "language": "es",
        "website": "https://www.infobae.com",
        "region": "Argentina"
    },
    
    # 🇩🇴 REPÚBLICA DOMINICANA
    "diario_libre": {
        "name": "Diario Libre RD",
        "url": "https://www.diariolibre.com/servicios/rss",
        "language": "es",
        "website": "https://www.diariolibre.com",
        "region": "República Dominicana"
    },
    "diario_libre_portada": {
        "name": "Diario Libre Portada",
        "url": "https://www.diariolibre.com/rss/portada.xml",
        "language": "es",
        "website": "https://www.diariolibre.com",
        "region": "República Dominicana"
    },
    "diario_libre_economia": {
        "name": "Diario Libre Economía",
        "url": "https://www.diariolibre.com/rss/economia.xml",
        "language": "es",
        "website": "https://www.diariolibre.com",
        "region": "República Dominicana"
    },
    "diario_libre_politica": {
        "name": "Diario Libre Política",
        "url": "https://www.diariolibre.com/rss/politica.xml",
        "language": "es",
        "website": "https://www.diariolibre.com",
        "region": "República Dominicana"
    },
    
    # 🇲🇽 MÉXICO (fuentes existentes)
    "el_universal": {
        "name": "El Universal México",
        "url": "https://www.eluniversal.com.mx/rss.xml",
        "language": "es",
        "website": "https://www.eluniversal.com.mx",
        "region": "México"
    },
    "elpais_america": {
        "name": "El País América",
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/america",
        "language": "es",
        "website": "https://elpais.com/america",
        "region": "México"
    }
}

# ---------- Función auxiliar para actualizar noticias ----------
def fetch_articles_from_source(source_key, limit=10, days_back=None, topic_filter=None):
    """
    Obtiene artículos de una fuente RSS específica
    
    Args:
        source_key: Clave de la fuente en RSS_SOURCES
        limit: Número máximo de artículos a procesar
        days_back: Solo procesar artículos de los últimos N días (None = todos)
        topic_filter: Filtrar por tema específico (None = todos)
    """
    if source_key not in RSS_SOURCES:
        raise ValueError(f"Fuente no válida: {source_key}")
    
    source = RSS_SOURCES[source_key]
    feed_url = source["url"]
    language = source["language"]
    
    feed = feedparser.parse(feed_url)
    nuevos = 0
    
    # Calcular fecha límite si se especifica days_back
    fecha_limite = None
    if days_back:
        from datetime import datetime, timedelta
        fecha_limite = datetime.utcnow() - timedelta(days=days_back)

    # Palabras clave para cada tema
    topic_keywords = {
        'economia': ['economía', 'económico', 'finanzas', 'dinero', 'inversión', 'mercado', 'bolsa', 'inflación', 'pib', 'desempleo', 'salario', 'presupuesto'],
        'politica': ['política', 'político', 'gobierno', 'presidente', 'ministro', 'congreso', 'senado', 'elecciones', 'votación', 'partido', 'democracia'],
        'salud': ['salud', 'médico', 'hospital', 'enfermedad', 'vacuna', 'covid', 'pandemia', 'tratamiento', 'medicina', 'cirugía', 'doctor'],
        'tecnologia': ['tecnología', 'tecnológico', 'digital', 'internet', 'software', 'hardware', 'aplicación', 'app', 'smartphone', 'computadora', 'inteligencia artificial'],
        'deportes': ['deporte', 'deportivo', 'fútbol', 'futbol', 'baloncesto', 'tenis', 'olímpico', 'mundial', 'campeonato', 'liga', 'equipo'],
        'cultura': ['cultura', 'cultural', 'arte', 'música', 'cine', 'película', 'libro', 'literatura', 'teatro', 'exposición', 'festival'],
        'internacional': ['internacional', 'mundial', 'global', 'país', 'nación', 'extranjero', 'diplomacia', 'onu', 'naciones unidas'],
        'nacional': ['nacional', 'local', 'región', 'ciudad', 'municipal', 'provincial', 'estatal'],
        'ciencia': ['ciencia', 'científico', 'investigación', 'estudio', 'descubrimiento', 'laboratorio', 'universidad', 'académico'],
        'medio_ambiente': ['medio ambiente', 'ambiental', 'clima', 'cambio climático', 'contaminación', 'sostenible', 'ecológico', 'naturaleza']
    }

    for entry in feed.entries[:limit]:
        url = entry.get("link")
        if not url or Article.query.filter_by(url=url).first():
            continue  # evitar duplicados

        titulo = entry.get("title")
        
        # Extraer fecha con múltiples formatos
        fecha = entry.get("published") or entry.get("pubDate") or entry.get("updated")
        fecha_iso = None
        fecha_dt = None
        if fecha:
            fecha_dt = dateparser.parse(fecha, languages=[language])
            if fecha_dt:
                fecha_iso = fecha_dt.strftime("%Y-%m-%dT%H:%M:%S")
        
        # Filtrar por fecha si se especifica days_back
        if fecha_limite and fecha_dt and fecha_dt < fecha_limite:
            continue  # Saltar artículos más antiguos que la fecha límite
        
        # Filtrar por tema si se especifica
        if topic_filter and topic_filter != "all":
            texto_completo = f"{titulo or ''} {entry.get('summary', '')}".lower()
            keywords = topic_keywords.get(topic_filter, [])
            if not any(keyword.lower() in texto_completo for keyword in keywords):
                continue  # Saltar artículos que no coincidan con el tema
        
        # Extraer autor
        autor = None
        if hasattr(entry, 'author') and entry.author:
            autor = entry.author
        elif hasattr(entry, 'authors') and entry.authors:
            autor = entry.authors[0] if entry.authors else None
        
        # Extraer sección/categoría
        seccion = None
        if hasattr(entry, 'tags') and entry.tags:
            seccion = entry.tags[0].term if entry.tags else None
        elif hasattr(entry, 'category') and entry.category:
            seccion = entry.category

        resumen = BeautifulSoup(entry.get("summary", ""), "html.parser").get_text(" ", strip=True)

        # Intentar extraer contenido extendido y datos adicionales
        contenido_ext = None
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=15)
            if r.ok:
                soup = BeautifulSoup(r.text, "html.parser")
                
                # Extraer contenido extendido
                ps = [p.get_text(" ", strip=True) for p in soup.find_all("p")]
                ps = [p for p in ps if len(p) > 30]
                if ps:
                    contenido_ext = " ".join(ps[:10])
                
                # Mejorar datos si no están disponibles desde RSS
                if not fecha_iso:
                    # Buscar fecha en meta tags
                    date_meta = (soup.find("meta", {"property": "article:published_time"}) or
                                soup.find("meta", {"name": "date"}) or
                                soup.find("meta", {"property": "og:updated_time"}))
                    if date_meta and date_meta.get("content"):
                        dt = dateparser.parse(date_meta["content"])
                        if dt:
                            fecha_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
                
                if not autor:
                    # Buscar autor en meta tags
                    author_meta = (soup.find("meta", {"name": "author"}) or
                                  soup.find("meta", {"property": "article:author"}) or
                                  soup.find("meta", {"name": "twitter:creator"}))
                    if author_meta and author_meta.get("content"):
                        autor = author_meta["content"].strip()
                
                if not seccion:
                    # Buscar sección en meta tags
                    section_meta = (soup.find("meta", {"property": "article:section"}) or
                                   soup.find("meta", {"name": "section"}) or
                                   soup.find("meta", {"property": "og:section"}))
                    if section_meta and section_meta.get("content"):
                        seccion = section_meta["content"].strip()
                
            time.sleep(0.5)  # Pequeño delay para evitar sobrecargar el servidor
        except Exception:
            pass

        # Procesar cada artículo individualmente para evitar bloqueos
        try:
            art = Article(
                url=url,
                title=titulo,
                date_iso=fecha_iso,
                summary=resumen,
                author=autor,
                section=seccion,
                content_long=contenido_ext,
                source=source_key,
                created_at=datetime.utcnow(),
            )
            db.session.add(art)
            db.session.commit()  # Commit individual para cada artículo
            nuevos += 1
        except Exception as e:
            db.session.rollback()
            print(f"Error guardando artículo {url}: {e}")
            continue

    return nuevos

@app.post("/refresh")
def refresh():
    try:
        source_key = request.form.get("source", "bbc_mundo")
        limit = int(request.form.get("limit", 10))  # Valor por defecto: 10 artículos
        days_back = request.form.get("days_back", 30)  # Valor por defecto: últimos 30 días
        topic_filter = request.form.get("topic", "all")  # Valor por defecto: todos los temas
        
        # Convertir days_back a entero si se proporciona
        if days_back and days_back != "all":
            days_back = int(days_back)
        else:
            days_back = 30  # Por defecto: últimos 30 días
        
        nuevos = fetch_articles_from_source(source_key, limit, days_back, topic_filter)
        source_name = RSS_SOURCES[source_key]["name"]
        
        # Mensaje con información del filtro aplicado
        tema_nombre = {
            'all': 'todos los temas',
            'economia': 'economía',
            'politica': 'política', 
            'salud': 'salud',
            'tecnologia': 'tecnología',
            'deportes': 'deportes',
            'cultura': 'cultura',
            'internacional': 'internacional',
            'nacional': 'nacional',
            'ciencia': 'ciencia',
            'medio_ambiente': 'medio ambiente'
        }.get(topic_filter, topic_filter)
        
        mensaje = f"Se actualizaron {nuevos} artículos nuevos desde {source_name} (últimos 30 días, tema: {tema_nombre})."
        
        if nuevos > 0:
            flash(mensaje, "ok")
        else:
            flash(f"No se encontraron artículos nuevos en {source_name} (últimos 30 días, tema: {tema_nombre}).", "ok")
    except Exception as e:
        db.session.rollback()
        flash(f"Error actualizando noticias: {e}", "error")
    return redirect(url_for("index"))

@app.post("/update-all")
def update_all_sources():
    """Actualiza todas las fuentes RSS disponibles"""
    try:
        import json
        from datetime import datetime
        
        data = request.get_json()
        limit = data.get('limit', 10)
        days_back = data.get('days_back', 30)
        
        # Fuentes que funcionan correctamente (basado en nuestras pruebas)
        working_sources = [
            'bbc_mundo',
            'el_tiempo_mundo', 
            'elpais_portada',
            'clarin',
            'diario_libre_portada',
            'diario_libre_economia',
            'diario_libre_politica'
        ]
        
        total_articles = 0
        sources_processed = 0
        errors = []
        
        for source_key in working_sources:
            try:
                nuevos = fetch_articles_from_source(source_key, limit, days_back)
                total_articles += nuevos
                sources_processed += 1
                print(f"✅ {RSS_SOURCES[source_key]['name']}: {nuevos} artículos nuevos")
            except Exception as e:
                error_msg = f"Error en {RSS_SOURCES[source_key]['name']}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
                continue
        
        # Preparar respuesta
        response_data = {
            'success': True,
            'total_articles': total_articles,
            'sources_processed': sources_processed,
            'total_sources': len(working_sources),
            'errors': errors
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@app.get("/download/csv")
def download_csv():
    """Descarga todos los artículos en formato CSV"""
    try:
        articles = Article.query.order_by(Article.created_at.desc()).all()
        
        def generate_csv():
            data = []
            yield "ID,Título,URL,Fecha,Autor,Sección,Fuente,Resumen,Contenido_extendido,Creado,Favorito\n"
            
            for article in articles:
                # Escapar comillas y comas para CSV
                title = (article.title or "").replace('"', '""')
                url = article.url or ""
                date_iso = article.date_iso or ""
                author = (article.author or "").replace('"', '""')
                section = (article.section or "").replace('"', '""')
                source = article.source or ""
                summary = (article.summary or "").replace('"', '""').replace('\n', ' ').replace('\r', ' ')
                content_long = (article.content_long or "").replace('"', '""').replace('\n', ' ').replace('\r', ' ')
                created = article.created_at.strftime('%Y-%m-%d %H:%M:%S') if article.created_at else ""
                favorite = "Sí" if article.is_favorite else "No"
                
                yield f'"{article.id}","{title}","{url}","{date_iso}","{author}","{section}","{source}","{summary}","{content_long}","{created}","{favorite}"\n'
        
        response = Response(generate_csv(), mimetype='text/csv')
        response.headers['Content-Disposition'] = f'attachment; filename=articulos_enriquecidos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        return response
        
    except Exception as e:
        flash(f"Error generando CSV: {e}", "error")
        return redirect(url_for("index"))

@app.get("/download/historical")
def download_historical():
    """Descarga artículos históricos con filtros de fecha"""
    try:
        # Parámetros de fecha
        days_back = int(request.args.get('days', 7))  # Por defecto últimos 7 días
        source_filter = request.args.get('source', '')  # Fuente específica
        format_type = request.args.get('format', 'csv')  # csv o json
        
        # Calcular fecha de inicio
        start_date = datetime.utcnow() - timedelta(days=days_back)
        
        # Construir consulta
        query = Article.query.filter(Article.created_at >= start_date)
        
        if source_filter:
            query = query.filter(Article.source == source_filter)
        
        articles = query.order_by(Article.created_at.desc()).all()
        
        if format_type == 'json':
            # Generar JSON
            data = []
            for article in articles:
                data.append({
                    'id': article.id,
                    'titulo': article.title,
                    'url': article.url,
                    'fecha': article.date_iso,
                    'autor': article.author,
                    'seccion': article.section,
                    'fuente': article.source,
                    'resumen': article.summary,
                    'contenido_extendido': article.content_long,
                    'creado': article.created_at.isoformat() if article.created_at else None,
                    'favorito': article.is_favorite
                })
            
            response = Response(
                json.dumps(data, ensure_ascii=False, indent=2),
                mimetype='application/json'
            )
            filename = f'articulos_historicos_{days_back}dias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        else:
            # Generar CSV
            def generate_csv():
                yield "ID,Título,URL,Fecha,Autor,Sección,Fuente,Resumen,Contenido_extendido,Creado,Favorito\n"
                
                for article in articles:
                    title = (article.title or "").replace('"', '""')
                    url = article.url or ""
                    date_iso = article.date_iso or ""
                    author = (article.author or "").replace('"', '""')
                    section = (article.section or "").replace('"', '""')
                    source = article.source or ""
                    summary = (article.summary or "").replace('"', '""').replace('\n', ' ').replace('\r', ' ')
                    content_long = (article.content_long or "").replace('"', '""').replace('\n', ' ').replace('\r', ' ')
                    created = article.created_at.strftime('%Y-%m-%d %H:%M:%S') if article.created_at else ""
                    favorite = "Sí" if article.is_favorite else "No"
                    
                    yield f'"{article.id}","{title}","{url}","{date_iso}","{author}","{section}","{source}","{summary}","{content_long}","{created}","{favorite}"\n'
            
            response = Response(generate_csv(), mimetype='text/csv')
            filename = f'articulos_historicos_{days_back}dias_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
        
    except Exception as e:
        flash(f"Error generando descarga histórica: {e}", "error")
        return redirect(url_for("index"))

@app.get("/download/by-date")
def download_by_date():
    """Descarga artículos por fecha específica"""
    try:
        date_str = request.args.get('date', '')  # Formato YYYY-MM-DD
        format_type = request.args.get('format', 'csv')
        
        if not date_str:
            flash("Debe especificar una fecha en formato YYYY-MM-DD", "error")
            return redirect(url_for("index"))
        
        # Parsear fecha
        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
            next_day = target_date + timedelta(days=1)
        except ValueError:
            flash("Formato de fecha inválido. Use YYYY-MM-DD", "error")
            return redirect(url_for("index"))
        
        # Consultar artículos del día específico
        articles = Article.query.filter(
            Article.created_at >= target_date,
            Article.created_at < next_day
        ).order_by(Article.created_at.desc()).all()
        
        if format_type == 'json':
            data = []
            for article in articles:
                data.append({
                    'id': article.id,
                    'titulo': article.title,
                    'url': article.url,
                    'fecha': article.date_iso,
                    'autor': article.author,
                    'seccion': article.section,
                    'fuente': article.source,
                    'resumen': article.summary,
                    'contenido_extendido': article.content_long,
                    'creado': article.created_at.isoformat() if article.created_at else None,
                    'favorito': article.is_favorite
                })
            
            response = Response(
                json.dumps(data, ensure_ascii=False, indent=2),
                mimetype='application/json'
            )
            filename = f'articulos_{date_str}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        else:
            def generate_csv():
                yield "ID,Título,URL,Fecha,Autor,Sección,Fuente,Resumen,Contenido_extendido,Creado,Favorito\n"
                
                for article in articles:
                    title = (article.title or "").replace('"', '""')
                    url = article.url or ""
                    date_iso = article.date_iso or ""
                    author = (article.author or "").replace('"', '""')
                    section = (article.section or "").replace('"', '""')
                    source = article.source or ""
                    summary = (article.summary or "").replace('"', '""').replace('\n', ' ').replace('\r', ' ')
                    content_long = (article.content_long or "").replace('"', '""').replace('\n', ' ').replace('\r', ' ')
                    created = article.created_at.strftime('%Y-%m-%d %H:%M:%S') if article.created_at else ""
                    favorite = "Sí" if article.is_favorite else "No"
                    
                    yield f'"{article.id}","{title}","{url}","{date_iso}","{author}","{section}","{source}","{summary}","{content_long}","{created}","{favorite}"\n'
            
            response = Response(generate_csv(), mimetype='text/csv')
            filename = f'articulos_{date_str}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
        
    except Exception as e:
        flash(f"Error generando descarga por fecha: {e}", "error")
        return redirect(url_for("index"))

@app.get("/download/json")
def download_json():
    """Descarga todos los artículos en formato JSON"""
    try:
        articles = Article.query.order_by(Article.created_at.desc()).all()
        
        data = []
        for article in articles:
            data.append({
                'id': article.id,
                'titulo': article.title,
                'url': article.url,
                'fecha': article.date_iso,
                'autor': article.author,
                'seccion': article.section,
                'fuente': article.source,
                'resumen': article.summary,
                'contenido_extendido': article.content_long,
                'creado': article.created_at.isoformat() if article.created_at else None
            })
        
        response = Response(
            json.dumps(data, ensure_ascii=False, indent=2),
            mimetype='application/json'
        )
        response.headers['Content-Disposition'] = f'attachment; filename=articulos_enriquecidos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        return response
        
    except Exception as e:
        flash(f"Error generando JSON: {e}", "error")
        return redirect(url_for("index"))

# ---------- Admin: ver DB rápida ----------
@app.get("/admin/db")
def admin_view_db():
    try:
        try:
            import pandas as pd  # import perezoso: solo cuando se usa la vista admin
        except Exception:
            return (
                "<pre>Para usar /admin/db necesitas instalar pandas:\n\n"
                "pip install pandas\n\n"
                "Luego vuelve a cargar esta ruta.</pre>",
                500,
            )
        conn = sqlite3.connect(str(DB_PATH))
        df_articles = pd.read_sql("SELECT * FROM articles ORDER BY created_at DESC LIMIT 50;", conn)
        df_links = pd.read_sql("SELECT * FROM links ORDER BY created_at DESC LIMIT 50;", conn)
        conn.close()

        styles = """
        <style>
          body{font-family:system-ui,Segoe UI,Roboto,sans-serif;background:#0b0f14;color:#eaf2fb;padding:24px}
          h1{font-size:1.4rem;margin:16px 0}
          .wrap{max-width:1200px;margin:0 auto}
          table{width:100%;border-collapse:collapse;font-size:0.92rem;background:#121821;border:1px solid #1c2530;border-radius:10px;overflow:hidden}
          th,td{border-bottom:1px solid #1c2530;padding:8px 10px;text-align:left;vertical-align:top}
          thead th{position:sticky;top:0;background:#0f1520}
          tbody tr:hover{background:#0f1520}
          .section{margin:22px 0}
        </style>
        """

        html = f"""
        {styles}
        <div class=wrap>
          <h1>Artículos (últimos 50)</h1>
          {df_articles.to_html(classes=["tbl"], index=False, border=0)}
          <div class=section></div>
          <h1>Links (últimos 50)</h1>
          {df_links.to_html(classes=["tbl"], index=False, border=0)}
        </div>
        """
        return html
    except Exception as e:
        return f"<pre>Error leyendo DB: {e}</pre>", 500

# ---------- Filtros Jinja ----------
@app.template_filter("short")
def short(s, n=140):
    if not s:
        return ""
    s = str(s)
    return s if len(s) <= n else s[:n].rstrip() + "…"

@app.template_filter("format_date")
def format_date(date_str):
    if not date_str:
        return ""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y')
    except:
        return date_str[:10] if len(date_str) >= 10 else date_str

# Agregar getattr como función global para las plantillas
@app.template_global()
def safe_getattr(obj, attr, default=None):
    return getattr(obj, attr, default)

# ---------- Eliminar registros ----------

@app.post("/delete-link/<int:link_id>")
def delete_link(link_id):
    try:
        link = Link.query.get_or_404(link_id)
        db.session.delete(link)
        db.session.commit()
        flash("Link eliminado.", "ok")
    except Exception as e:
        db.session.rollback()
        flash(f"Error eliminando link: {e}", "error")
    return redirect(url_for("index"))

@app.post("/delete-article/<int:article_id>")
def delete_article(article_id):
    try:
        art = Article.query.get_or_404(article_id)
        db.session.delete(art)
        db.session.commit()
        flash("Artículo eliminado.", "ok")
    except Exception as e:
        db.session.rollback()
        flash(f"Error eliminando artículo: {e}", "error")
    return redirect(url_for("index"))

# ---------- Sistema de Favoritos ----------
@app.post("/toggle-favorite/<int:article_id>")
def toggle_favorite(article_id):
    try:
        article = Article.query.get_or_404(article_id)
        # Toggle el estado del favorito
        article.is_favorite = not (article.is_favorite or False)
        db.session.commit()
        
        status = "favorito" if article.is_favorite else "no favorito"
        flash(f"Artículo marcado como {status}.", "ok")
    except Exception as e:
        db.session.rollback()
        flash(f"Error actualizando favorito: {e}", "error")
    return redirect(url_for("index"))

# ---------- Búsqueda Avanzada ----------
@app.get("/search")
def search():
    query = request.args.get('q', '').strip()
    source = request.args.get('source', '')
    author = request.args.get('author', '')
    section = request.args.get('section', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    articles = Article.query
    
    if query:
        articles = articles.filter(
            db.or_(
                Article.title.contains(query),
                Article.summary.contains(query),
                Article.content_long.contains(query)
            )
        )
    
    if source:
        articles = articles.filter(Article.source == source)
    
    if author:
        articles = articles.filter(Article.author.contains(author))
    
    if section:
        articles = articles.filter(Article.section.contains(section))
    
    if date_from:
        try:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            articles = articles.filter(Article.created_at >= from_date)
        except:
            pass
    
    if date_to:
        try:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            articles = articles.filter(Article.created_at <= to_date)
        except:
            pass
    
    results = articles.order_by(Article.created_at.desc()).all()
    
    return render_template("search.html", 
                         results=results, 
                         query=query,
                         source=source,
                         author=author,
                         section=section,
                         date_from=date_from,
                         date_to=date_to,
                         rss_sources=RSS_SOURCES)

# ---------- API REST ----------
@app.get("/api/articles")
def api_articles():
    """API REST para obtener artículos con paginación"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    source = request.args.get('source', '')
    
    query = Article.query
    if source:
        query = query.filter(Article.source == source)
    
    articles = query.order_by(Article.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return {
        'articles': [{
            'id': a.id,
            'title': a.title,
            'url': a.url,
            'date': a.date_iso,
            'author': a.author,
            'section': a.section,
            'source': a.source,
            'summary': a.summary,
            'created_at': a.created_at.isoformat() if a.created_at else None
        } for a in articles.items],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': articles.total,
            'pages': articles.pages,
            'has_next': articles.has_next,
            'has_prev': articles.has_prev
        }
    }

# ---------- Acciones en Lote ----------
@app.post("/bulk-action")
def bulk_action():
    action = request.form.get('action')
    article_ids = request.form.getlist('article_ids')
    
    if not article_ids:
        flash("No se seleccionaron artículos.", "error")
        return redirect(url_for("index"))
    
    try:
        if action == 'delete':
            Article.query.filter(Article.id.in_(article_ids)).delete(synchronize_session=False)
            db.session.commit()
            flash(f"Se eliminaron {len(article_ids)} artículos.", "ok")
        elif action == 'mark_favorite':
            Article.query.filter(Article.id.in_(article_ids)).update({'is_favorite': True}, synchronize_session=False)
            db.session.commit()
            flash(f"Se marcaron {len(article_ids)} artículos como favoritos.", "ok")
        elif action == 'unmark_favorite':
            Article.query.filter(Article.id.in_(article_ids)).update({'is_favorite': False}, synchronize_session=False)
            db.session.commit()
            flash(f"Se desmarcaron {len(article_ids)} artículos como favoritos.", "ok")
    except Exception as e:
        db.session.rollback()
        flash(f"Error en acción masiva: {e}", "error")
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Ejecuta: python app.py  (se abrirá en http://127.0.0.1:8000/)
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="127.0.0.1", port=port, debug=True)
