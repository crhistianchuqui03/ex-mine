#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar las fuentes RSS que funcionan correctamente
"""

import requests
import feedparser
from bs4 import BeautifulSoup
import time

# Fuentes que funcionan correctamente
WORKING_SOURCES = {
    "bbc_mundo": {
        "name": "BBC Mundo",
        "url": "https://feeds.bbci.co.uk/mundo/rss.xml",
        "language": "es",
        "website": "https://www.bbc.com/mundo",
        "region": "Internacional"
    },
    "el_tiempo_mundo": {
        "name": "El Tiempo Mundo",
        "url": "https://www.eltiempo.com/rss/mundo.xml",
        "language": "es",
        "website": "https://www.eltiempo.com",
        "region": "Colombia"
    },
    "elpais_portada": {
        "name": "El País Portada",
        "url": "https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/portada",
        "language": "es",
        "website": "https://elpais.com",
        "region": "España"
    },
    "clarin": {
        "name": "Clarín Argentina",
        "url": "https://www.clarin.com/rss/lo-ultimo/",
        "language": "es",
        "website": "https://www.clarin.com",
        "region": "Argentina"
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
    }
}

def test_working_sources():
    print("🎯 Probando fuentes RSS que funcionan correctamente...")
    print("=" * 60)
    
    total_articles = 0
    working_sources = 0
    
    for key, source_info in WORKING_SOURCES.items():
        name = source_info["name"]
        url = source_info["url"]
        region = source_info["region"]
        
        print(f"\n🔍 {region} - {name}")
        print(f"   URL: {url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                article_count = len(feed.entries)
                total_articles += article_count
                working_sources += 1
                
                print(f"   ✅ {article_count} artículos encontrados")
                
                # Mostrar algunos títulos de ejemplo
                for i, entry in enumerate(feed.entries[:3]):
                    title = entry.get('title', 'Sin título')[:60]
                    print(f"      {i+1}. {title}...")
                    
                # Mostrar información adicional si está disponible
                if hasattr(feed, 'feed') and feed.feed:
                    if hasattr(feed.feed, 'title'):
                        print(f"   📰 Feed: {feed.feed.title}")
                    if hasattr(feed.feed, 'description'):
                        desc = feed.feed.description[:100] if feed.feed.description else "Sin descripción"
                        print(f"   📝 Descripción: {desc}...")
            else:
                print("   ❌ No se encontraron entradas")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Pausa para no sobrecargar los servidores
    
    print("\n" + "=" * 60)
    print(f"📊 Resumen:")
    print(f"   • Fuentes funcionando: {working_sources}/{len(WORKING_SOURCES)}")
    print(f"   • Total de artículos: {total_articles}")
    print(f"   • Promedio por fuente: {total_articles/working_sources:.1f}" if working_sources > 0 else "   • Promedio por fuente: 0")
    
    if working_sources == len(WORKING_SOURCES):
        print("🎉 ¡Todas las fuentes funcionan perfectamente!")
    else:
        print("⚠️  Algunas fuentes tienen problemas")

if __name__ == "__main__":
    test_working_sources()
