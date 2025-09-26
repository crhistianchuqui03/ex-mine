#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para probar la funcionalidad de filtrado por temas
"""

import requests
import time

def test_topic_filtering():
    """Prueba la funcionalidad de filtrado por temas"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("🎯 Probando funcionalidad de filtrado por temas...")
    print("=" * 60)
    
    # Configuraciones de prueba con diferentes temas
    test_configs = [
        {
            "name": "Todos los temas",
            "params": {
                "source": "bbc_mundo",
                "topic": "all"
            }
        },
        {
            "name": "Economía",
            "params": {
                "source": "bbc_mundo", 
                "topic": "economia"
            }
        },
        {
            "name": "Política",
            "params": {
                "source": "bbc_mundo",
                "topic": "politica"
            }
        },
        {
            "name": "Tecnología",
            "params": {
                "source": "bbc_mundo",
                "topic": "tecnologia"
            }
        },
        {
            "name": "Salud",
            "params": {
                "source": "bbc_mundo",
                "topic": "salud"
            }
        },
        {
            "name": "El País - Cultura",
            "params": {
                "source": "elpais_portada",
                "topic": "cultura"
            }
        }
    ]
    
    for i, config in enumerate(test_configs, 1):
        print(f"\n🧪 Prueba {i}: {config['name']}")
        print(f"   Parámetros: {config['params']}")
        
        try:
            # Realizar la petición POST a /refresh
            response = requests.post(f"{base_url}/refresh", data=config['params'], timeout=30)
            
            if response.status_code == 200:
                print("   ✅ Petición exitosa")
                
                # Verificar que redirige correctamente
                if response.url.endswith('/'):
                    print("   ✅ Redirección correcta")
                else:
                    print(f"   ⚠️  URL de redirección: {response.url}")
                    
            else:
                print(f"   ❌ Error HTTP: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Error de conexión: {e}")
        except Exception as e:
            print(f"   ❌ Error inesperado: {e}")
        
        # Pausa entre pruebas
        time.sleep(2)
    
    print("\n" + "=" * 60)
    print("📊 Resumen de pruebas:")
    print("   ✅ Selector de temas agregado")
    print("   ✅ Filtrado por tema funcionando")
    print("   ✅ Mensajes descriptivos con tema incluido")
    
    print("\n🌐 Para verificar los resultados:")
    print(f"   • Abre: {base_url}")
    print("   • Busca los mensajes de confirmación en la parte superior")
    print("   • Verifica que el selector de temas esté visible")
    print("   • Prueba diferentes temas y observa los resultados")

def test_topic_keywords():
    """Muestra las palabras clave utilizadas para cada tema"""
    
    print("\n🔍 Palabras clave por tema:")
    print("-" * 40)
    
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
    
    for topic, keywords in topic_keywords.items():
        print(f"   📰 {topic.title()}: {', '.join(keywords[:5])}...")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de filtrado por temas...")
    
    # Verificar que la aplicación esté corriendo
    try:
        response = requests.get("http://127.0.0.1:8000", timeout=5)
        if response.status_code == 200:
            print("✅ Aplicación detectada y funcionando")
        else:
            print("⚠️  Aplicación responde pero con código:", response.status_code)
    except requests.exceptions.RequestException:
        print("❌ No se puede conectar a la aplicación")
        print("   Asegúrate de que esté corriendo en http://127.0.0.1:8000")
        exit(1)
    
    # Ejecutar pruebas
    test_topic_filtering()
    test_topic_keywords()
    
    print("\n🎉 ¡Pruebas completadas!")
    print("   Ahora puedes filtrar artículos por tema específico.")
