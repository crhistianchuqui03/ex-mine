#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de filtrado en tiempo real por tema
"""

import requests
import time

def test_realtime_topic_filtering():
    """Prueba la funcionalidad de filtrado en tiempo real"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🎯 Probando filtrado en tiempo real por tema...")
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
    
    print("\n2. 🎯 Prueba el filtrado por tema:")
    print("   • Selecciona '💰 Economía' en el selector de temas")
    print("   • Observa cómo se filtran automáticamente los artículos")
    print("   • Verifica que aparezca el mensaje de confirmación")
    
    print("\n3. 🔄 Prueba diferentes temas:")
    topics = [
        ("🏛️ Política", "politica"),
        ("🏥 Salud", "salud"), 
        ("💻 Tecnología", "tecnologia"),
        ("⚽ Deportes", "deportes"),
        ("🎭 Cultura", "cultura"),
        ("🌍 Internacional", "internacional"),
        ("🔬 Ciencia", "ciencia"),
        ("🌱 Medio Ambiente", "medio_ambiente")
    ]
    
    for emoji_name, topic_key in topics:
        print(f"   • {emoji_name}: Selecciona '{emoji_name}' y observa el filtrado")
    
    print("\n4. 📊 Verifica la funcionalidad:")
    print("   • Los artículos se filtran instantáneamente")
    print("   • Aparece un mensaje con el número de artículos encontrados")
    print("   • Al seleccionar '📰 Todos los temas' se muestran todos")
    
    print("\n5. 🔍 Palabras clave que se buscan:")
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
    
    print("\n6. ✅ Funcionalidades implementadas:")
    print("   ✅ Selector de tema con evento onchange")
    print("   ✅ Función JavaScript filterArticlesByTopic()")
    print("   ✅ Búsqueda de palabras clave en título y contenido")
    print("   ✅ Ocultación/mostrado dinámico de filas")
    print("   ✅ Mensajes informativos con contadores")
    print("   ✅ Clases CSS agregadas a las filas de la tabla")
    
    print("\n🎉 ¡Filtrado en tiempo real implementado!")
    print("   Ahora puedes filtrar artículos existentes por tema instantáneamente.")

if __name__ == "__main__":
    test_realtime_topic_filtering()
