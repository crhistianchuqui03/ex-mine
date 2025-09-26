#!/usr/bin/env python3
"""
Script de demostración para las funcionalidades de descarga histórica
"""

import requests
import json
from datetime import datetime, timedelta

def demo_historical_downloads():
    """Demuestra las nuevas funcionalidades de descarga histórica"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🎯 DEMOSTRACIÓN: Descarga de Datos Históricos")
    print("=" * 60)
    
    # 1. Descarga histórica - últimos 7 días
    print("\n📅 1. Descarga histórica - Últimos 7 días")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/download/historical?days=7&format=json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Descargados {len(data)} artículos de los últimos 7 días")
            
            # Mostrar algunos ejemplos
            if data:
                print("\n📰 Ejemplos de artículos:")
                for i, article in enumerate(data[:3]):
                    print(f"   {i+1}. {article['titulo'][:50]}...")
                    print(f"      Fuente: {article['fuente']}")
                    print(f"      Fecha: {article['creado'][:10]}")
                    print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Descarga por fuente específica
    print("\n📰 2. Descarga por fuente específica - BBC Mundo")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/download/historical?days=3&source=bbc_mundo&format=csv", timeout=10)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            print(f"✅ Descargados {len(lines)-1} artículos de BBC Mundo (últimos 3 días)")
            print("   Formato: CSV")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Descarga por fecha específica
    print("\n📆 3. Descarga por fecha específica")
    print("-" * 40)
    
    # Usar fecha de ayer
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    try:
        response = requests.get(f"{base_url}/download/by-date?date={yesterday}&format=json", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Descargados {len(data)} artículos del {yesterday}")
            
            if data:
                print("\n📰 Artículos del día:")
                for i, article in enumerate(data[:2]):
                    print(f"   {i+1}. {article['titulo'][:40]}...")
                    print(f"      Autor: {article['autor']}")
                    print(f"      Sección: {article['seccion']}")
                    print()
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Estadísticas de la base de datos
    print("\n📊 4. Estadísticas de la base de datos")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/articles?per_page=100", timeout=10)
        if response.status_code == 200:
            data = response.json()
            articles = data['articles']
            
            print(f"✅ Total de artículos disponibles: {len(articles)}")
            
            # Contar por fuente
            sources = {}
            for article in articles:
                source = article['source'] or 'Manual'
                sources[source] = sources.get(source, 0) + 1
            
            print("\n📰 Distribución por fuente:")
            for source, count in sources.items():
                print(f"   • {source}: {count} artículos")
            
            # Contar favoritos
            favorites = sum(1 for article in articles if article.get('favorito'))
            print(f"\n⭐ Artículos favoritos: {favorites}")
            
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. URLs de descarga disponibles
    print("\n🔗 5. URLs de descarga disponibles")
    print("-" * 40)
    
    print("📥 Descargas históricas:")
    print(f"   • Últimos 7 días (CSV): {base_url}/download/historical?days=7&format=csv")
    print(f"   • Últimos 7 días (JSON): {base_url}/download/historical?days=7&format=json")
    print(f"   • Últimos 30 días (CSV): {base_url}/download/historical?days=30&format=csv")
    print(f"   • BBC Mundo últimos 3 días: {base_url}/download/historical?days=3&source=bbc_mundo&format=csv")
    
    print("\n📆 Descargas por fecha:")
    print(f"   • Por fecha específica (CSV): {base_url}/download/by-date?date=YYYY-MM-DD&format=csv")
    print(f"   • Por fecha específica (JSON): {base_url}/download/by-date?date=YYYY-MM-DD&format=json")
    
    print("\n📊 Descargas completas:")
    print(f"   • Todos los artículos (CSV): {base_url}/download/csv")
    print(f"   • Todos los artículos (JSON): {base_url}/download/json")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Demostración completada!")
    print("\n💡 Consejos de uso:")
    print("   • Usa la interfaz web para descargas interactivas")
    print("   • Los archivos se descargan automáticamente")
    print("   • Los nombres incluyen fecha y hora de descarga")
    print("   • Puedes filtrar por fuente y período específico")
    print("   • Los datos incluyen información de favoritos")

def main():
    """Función principal"""
    try:
        demo_historical_downloads()
    except Exception as e:
        print(f"❌ Error durante la demostración: {e}")

if __name__ == "__main__":
    main()
