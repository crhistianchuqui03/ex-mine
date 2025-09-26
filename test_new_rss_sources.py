#!/usr/bin/env python3
"""
Script para probar todas las nuevas fuentes RSS agregadas
"""

import requests
import feedparser
import time
from datetime import datetime

def test_rss_source(name, url):
    """Probar una fuente RSS específica"""
    print(f"🔍 Probando: {name}")
    print(f"   URL: {url}")
    
    try:
        # Intentar parsear el feed
        feed = feedparser.parse(url)
        
        if feed.bozo:
            print(f"   ⚠️  Feed con problemas de formato")
        
        if not feed.entries:
            print(f"   ❌ No se encontraron entradas")
            return False
        
        print(f"   ✅ {len(feed.entries)} entradas encontradas")
        
        # Mostrar algunas entradas de ejemplo
        for i, entry in enumerate(feed.entries[:3]):
            title = entry.get('title', 'Sin título')[:50]
            print(f"      {i+1}. {title}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Probar todas las fuentes RSS"""
    print("🌍 Probando todas las fuentes RSS agregadas...")
    print("=" * 60)
    
    # Fuentes RSS organizadas por región
    sources = {
        # 🌍 INTERNACIONALES
        "BBC Mundo": "https://feeds.bbci.co.uk/mundo/rss.xml",
        "CNN en Español": "https://cnnespanol.cnn.com/feed/",
        "Voz de América": "https://www.vozdeamerica.com/rssfeeds",
        "Latinvex": "https://latinvex.com/latinvex-rss/",
        "Noticias Latinas": "https://www.noticias-latinas.net/rss/listado/",
        
        # 🇵🇪 PERÚ
        "El Comercio Perú": "https://elcomercio.pe/rss/",
        "El Perfil Perú": "https://elperfil.pe/canales-rss/",
        "RPP Noticias": "https://rpp.pe/noticias/rss",
        "Perú21": "https://peru21.pe/",
        "Diario Perú": "https://diarioperu.pe/",
        "El Heraldo Perú": "https://elheraldo.pe/",
        
        # 🇨🇴 COLOMBIA
        "El Tiempo Colombia": "https://www.eltiempo.com/rss",
        "El Tiempo Mundo": "https://www.eltiempo.com/rss/mundo.xml",
        
        # 🇪🇸 ESPAÑA
        "El País España": "https://elpais.com/info/rss/",
        "El País Portada": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
        "El Mundo España": "https://rss.elmundo.es/rss/",
        
        # 🇦🇷 ARGENTINA
        "Clarín Argentina": "https://www.clarin.com/rss/lo-ultimo/",
        "MinutoUno Argentina": "https://www.minutouno.com/rss",
        "Infobae Argentina": "https://www.infobae.com/feeds/rss/",
        
        # 🇩🇴 REPÚBLICA DOMINICANA
        "Diario Libre RD": "https://www.diariolibre.com/servicios/rss",
        "Diario Libre Portada": "https://www.diariolibre.com/rss/portada.xml",
        "Diario Libre Economía": "https://www.diariolibre.com/rss/economia.xml",
        "Diario Libre Política": "https://www.diariolibre.com/rss/politica.xml",
        
        # 🇲🇽 MÉXICO
        "El Universal México": "https://www.eluniversal.com.mx/rss.xml",
        "El País América": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/america"
    }
    
    successful = 0
    total = len(sources)
    
    for name, url in sources.items():
        if test_rss_source(name, url):
            successful += 1
        print()  # Línea en blanco
        time.sleep(1)  # Pausa entre pruebas
    
    print("=" * 60)
    print(f"📊 Resumen: {successful}/{total} fuentes funcionando correctamente")
    
    if successful == total:
        print("🎉 ¡Todas las fuentes RSS están funcionando!")
    elif successful > total * 0.8:
        print("✅ La mayoría de fuentes están funcionando correctamente")
    else:
        print("⚠️  Algunas fuentes pueden tener problemas")

if __name__ == "__main__":
    main()
