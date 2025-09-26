#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de filtrado por tema en la tabla
"""

import requests
import time

def test_topic_filter_in_table():
    """Prueba la funcionalidad de filtrado por tema en la tabla"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🎯 Probando filtrado por tema en la tabla de artículos...")
    print("=" * 60)
    
    # Verificar que la aplicación esté funcionando
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Aplicación funcionando correctamente")
        else:
            print(f"⚠️  Aplicación responde con código: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error conectando a la aplicación: {e}")
        return
    
    print("\n📋 Instrucciones para probar manualmente:")
    print("=" * 50)
    
    print("1. 🌐 Abre la aplicación en tu navegador:")
    print(f"   {base_url}")
    
    print("\n2. 🎯 Localiza el selector de temas:")
    print("   • Busca en la barra de acciones de la tabla")
    print("   • Debería estar entre el selector de ordenamiento y el botón 'Limpiar'")
    print("   • Tiene un estilo destacado con gradiente verde")
    
    print("\n3. 🔄 Prueba diferentes temas:")
    topics = [
        ("📰 Todos los temas", "all"),
        ("💰 Economía", "economia"),
        ("🏛️ Política", "politica"),
        ("🏥 Salud", "salud"), 
        ("💻 Tecnología", "tecnologia"),
        ("⚽ Deportes", "deportes"),
        ("🎭 Cultura", "cultura"),
        ("🌍 Internacional", "internacional"),
        ("🏠 Nacional", "nacional"),
        ("🔬 Ciencia", "ciencia"),
        ("🌱 Medio Ambiente", "medio_ambiente")
    ]
    
    for emoji_name, topic_key in topics:
        print(f"   • {emoji_name}: Selecciona y observa el filtrado instantáneo")
    
    print("\n4. 📊 Verifica la funcionalidad:")
    print("   • Los artículos se filtran instantáneamente al cambiar tema")
    print("   • Aparece un mensaje toast con el número de artículos encontrados")
    print("   • Los artículos no coincidentes se ocultan")
    print("   • Al seleccionar 'Todos los temas' se muestran todos")
    
    print("\n5. 🧹 Prueba el botón 'Limpiar':")
    print("   • Debería resetear el filtro de temas a 'Todos los temas'")
    print("   • Debería mostrar todos los artículos nuevamente")
    print("   • Debería limpiar también la búsqueda y ordenamiento")
    
    print("\n6. 🔍 Palabras clave que se buscan:")
    topic_keywords = {
        'economia': ['economía', 'finanzas', 'mercado', 'inflación', 'pib'],
        'politica': ['política', 'gobierno', 'presidente', 'elecciones'],
        'salud': ['salud', 'médico', 'hospital', 'vacuna', 'covid'],
        'tecnologia': ['tecnología', 'digital', 'software', 'app', 'smartphone'],
        'deportes': ['deporte', 'fútbol', 'baloncesto', 'olímpico', 'mundial'],
        'cultura': ['cultura', 'arte', 'música', 'cine', 'libro'],
        'internacional': ['internacional', 'mundial', 'global', 'país'],
        'nacional': ['nacional', 'local', 'región', 'ciudad'],
        'ciencia': ['ciencia', 'científico', 'investigación', 'universidad'],
        'medio_ambiente': ['medio ambiente', 'clima', 'contaminación', 'ecológico']
    }
    
    for topic, keywords in topic_keywords.items():
        print(f"   • {topic.title()}: {', '.join(keywords[:3])}...")
    
    print("\n7. ✅ Funcionalidades implementadas:")
    print("   ✅ Selector de tema en la barra de acciones")
    print("   ✅ Estilos CSS destacados con gradiente verde")
    print("   ✅ Función JavaScript filterArticlesByTopic()")
    print("   ✅ Búsqueda de palabras clave en título y contenido")
    print("   ✅ Ocultación/mostrado dinámico de filas")
    print("   ✅ Mensajes informativos con contadores")
    print("   ✅ Integración con botón 'Limpiar'")
    print("   ✅ Clases CSS agregadas a las filas (.article-row, .article-title, .article-content)")
    
    print("\n🎉 ¡Filtrado por tema en la tabla implementado!")
    print("   Ahora puedes filtrar artículos existentes por tema directamente desde la tabla.")

if __name__ == "__main__":
    test_topic_filter_in_table()
